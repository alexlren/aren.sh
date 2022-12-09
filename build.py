#! /usr/bin/env python3

import argparse, datetime, json, os, shutil, subprocess, sys, yaml
from functools import reduce
from collections import defaultdict
from os import path
from tempfile import mkdtemp

SRC_DIRNAME = 'posts'
TEMPLATE_DIRNAME = 'templates'
PUBLIC_DIRNAME = 'public'

CURDIR = path.dirname(path.realpath(__file__))
BUILDDIR = path.join(CURDIR, '.build')
SRCDIR = path.join(CURDIR, SRC_DIRNAME)
TEMPLATEDIR = path.join(CURDIR, TEMPLATE_DIRNAME)
PUBLICDIR = path.join(CURDIR, PUBLIC_DIRNAME)


def get_pandoc_options(template, metadata):
    title = metadata['title']
    categories = metadata['categories']
    menu = ' '.join(sorted((f'--metadata="categories:{catname}"' for catname in categories)))
    variables = ' '.join((f'--variable="{k}:{v}"' for k, v in metadata['variables'].items()))
    options = " --defaults=./pandoc.yaml" \
        f" {menu}" \
        f" --metadata=\"pagetitle:{title}\"" \
        f" --template=\"{template}\"" \
        f" {variables}"
    return options


def get_html_content(infile):
    body = subprocess.check_output(f'pandoc "{infile}" -t html', shell=True)
    return body.decode('utf-8')


def build_rss_feed(posts):
    def rss_date(date_str):
        year, month, day = (int(d) for d in date_str.split('/'))
        date = datetime.date(year, month, day)
        return date.strftime('%a, %d %b %Y 00:00:00 +0000')

    # Retrieve metadata
    with open('./metadata.yaml', 'r') as f:
        metadata = yaml.safe_load(f)

    pub_date = rss_date(posts[0]['date'])
    build_date = datetime.date.today().strftime("%a, %d %b %Y %H:%M:%S %z")
    item_tmpl = """
<item>
  <title>{title}</title>
  <description><![CDATA[{description}]]></description>
  <link>{site_url}{url}</link>
  <guid>{url}</guid>
  <pubDate>{pub_date}</pubDate>
</item>
"""
    feed_tmpl = """<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">
<channel>
  <title>{site_name}</title>
  <link>{site_url}/feed.xml</link>
  <description><![CDATA[{description}]]></description>
  <image>
      <url>{site_url}/img/logo.png</url>
      <title>{site_name} logo</title>
      <link>{site_url}</link>
  </image>
  <lastBuildDate>{build_date}</lastBuildDate>
  <pubDate>{pub_date}</pubDate>
  {items}
</channel>
</rss>
"""
    items = '\n'.join((item_tmpl.format(
        title=p['title'],
        site_url=metadata['site_url'],
        url=p['url'],
        description=get_html_content(p['path']),
        pub_date=rss_date(p['date'])
    ) for p in posts))

    outfile = path.join(BUILDDIR, 'feed.xml')
    print(f'Build rss feed -> {outfile}')
    with open(outfile, 'w') as fd:
        fd.write(feed_tmpl.format(
            build_date=build_date,
            pub_date=pub_date,
            items=items,
            site_url=metadata['site_url'],
            site_name=metadata['site_name'],
            description=metadata['site_description'],
    ))


def build_index(outfile, name, posts, options):
    posts.sort(key=lambda x: x['date'], reverse=True)
    groups_per_year = defaultdict(list)
    for post in posts:
        year = post['date'].split('/')[0]
        groups_per_year[year].append(post)
    # necessary because defaultdict cannot be sorted
    group_keys = sorted(groups_per_year.items(), reverse=True)
    md='---\nlist: ' + json.dumps(group_keys) + '\n---\n'
    outdir = path.dirname(outfile)
    print(f'Build {name} index -> {outfile}')
    os.makedirs(outdir, exist_ok=True)
    metadata = {
        'title': name,
        'categories': options['categories'],
        'variables': {
            'build_msg': options['build_msg'],
            'category': options.get('category', ''),
        },
    }
    options = get_pandoc_options('index', metadata)
    subprocess.Popen(f"""printf "%s" '{md}' | pandoc {options} -o {outfile}""", shell=True).wait()


def build_metadata_from(mdfilename, name, options):
    with open(mdfilename, 'r') as md:
        content = md.read()
        y = content.split('---')[1]
        metadata = yaml.safe_load(y)
        metadata['categories'] = options['categories']
        metadata['variables'] = {
            'build_msg': options['build_msg'],
            'category': path.basename(path.dirname(mdfilename)),
        }
        metadata['url'] = '/{}/{}.html'.format(metadata['date'], name)
        metadata['path'] = mdfilename
        return metadata
    return None


def build_page(mdfilename, options):
    (name, ext) = path.splitext(path.basename(mdfilename))
    if ext != '.md' or name.startswith('.#'):
        return
    # Get all metadata as json
    metadata = build_metadata_from(mdfilename, name, options)
    outfile = BUILDDIR + metadata['url']
    tmpdir = mkdtemp()
    tmpfile = tmpdir + metadata['url']
    try:
        os.makedirs(path.dirname(tmpfile), exist_ok=True)
        os.makedirs(path.dirname(outfile), exist_ok=True)
        print(f'Build page -> {tmpfile}')
        options = get_pandoc_options('article', metadata)
        subprocess.Popen(f"pandoc {mdfilename} {options} -o {tmpfile}", shell=True).wait()
        print(f'Post process page {tmpfile} -> {outfile}')
        subprocess.Popen(f"node tools/tex2chtml.js {tmpfile} {outfile}", shell=True).wait()
        return metadata
    except Exception as err:
        shutil.rmtree(tmpdir)
        raise err


def build_assets():
    print(f'Copy assets -> {BUILDDIR}')
    shutil.copytree(PUBLICDIR, BUILDDIR, dirs_exist_ok=True)


def build_categories_index(pages, options):
    page_groups = reduce(lambda grp, page: grp[page['variables']['category']].append(page) or grp, pages, defaultdict(list))
    for category, posts in page_groups.items():
        outfile = path.join(BUILDDIR, category, 'index.html')
        build_index(outfile, category, posts, {**options, 'category': category})


def build_tags_index(pages, options):
    page_groups = {}
    for page in pages:
        for tag in page['tags']:
            page_groups.setdefault(tag, [])
            page_groups[tag].append(page)
    for tag, posts in page_groups.items():
        outfile = path.join(BUILDDIR, 'tag', f'{tag}.html')
        build_index(outfile, tag, posts, options)


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--build-msg', type=str,
        default='',
        help='Message displayed at the bottom of the pages',
    )

    args = parser.parse_args()

    categories = os.listdir(SRCDIR)
    pages = []
    options = {
        'build_msg': args.build_msg,
        'categories': sorted(categories),
    }

    # Build pages
    for category in categories:
        catdir = path.join(SRCDIR, category)
        posts = os.listdir(catdir)

        for postfilename in posts:
            post = path.join(catdir, postfilename)
            page = build_page(post, options)
            pages.append(page)

    # JS / CSS / Images / Fonts
    build_assets()
    # Build <category>/index.html
    build_categories_index(pages, options)
    # Build tag/<tag>.html
    build_tags_index(pages, options)
    # Build index.html
    build_index(path.join(BUILDDIR, 'index.html'), 'index', pages, options)
    # Build feed.xml
    build_rss_feed(pages)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
