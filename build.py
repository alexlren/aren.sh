#! /usr/bin/env python3

import datetime, json, os, shutil, subprocess, sys


SRC_DIRNAME = 'posts'
TEMPLATE_DIRNAME = 'templates'
PUBLIC_DIRNAME = 'public'

CURDIR = os.path.dirname(os.path.realpath(__file__))
BUILDDIR = os.path.join(CURDIR, '.build')
SRCDIR = os.path.join(CURDIR, SRC_DIRNAME)
TEMPLATEDIR = os.path.join(CURDIR, TEMPLATE_DIRNAME)
PUBLICDIR = os.path.join(CURDIR, PUBLIC_DIRNAME)


def get_pandoc_options(outfile, template, context):
    title = context['title']
    menu = context['menu']
    variables = ' '.join((f'--variable="{k}:{v}"' for k, v in context['variables'].items()))
    options = " --defaults=./pandoc.yaml" \
        f" {menu}" \
        f" --metadata=\"pagetitle:{title}\"" \
        f" -o \"{outfile}\"" \
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
        site_url=p['site_url'],
        url=p['url'],
        description=get_html_content(p['infile']),
        pub_date=rss_date(p['date'])
    ) for p in posts))

    outfile = os.path.join(BUILDDIR, 'feed.xml')
    print(f'Build rss feed -> {outfile}')
    with open(outfile, 'w') as fd:
        fd.write(feed_tmpl.format(
            build_date=build_date,
            pub_date=pub_date,
            items=items,
            site_url=posts[0]['site_url'],
            site_name=posts[0]['site_name'],
            description=posts[0]['site_description'],
    ))

def build_index(dirname, name, posts, context):
    posts.sort(key=lambda x: x['date'], reverse=True)
    md='---\nlist: ' + json.dumps(posts) + '\n---\n'
    outdir = os.path.join(BUILDDIR, dirname)
    outfile = os.path.join(outdir, name + '.html')
    if dirname != '':
        title = dirname + ' / ' + name
    else:
        title = name
    print(f'Build {name} index -> {outfile}')
    os.makedirs(outdir, exist_ok=True)
    context['title'] = title
    context['variables']['title'] = title
    context['variables']['category'] = name
    options = get_pandoc_options(outfile, 'index', context)
    subprocess.Popen(f"""printf "%s" '{md}' | pandoc {options}""", shell=True).wait()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        build_msg = sys.argv[1]
    else:
        build_msg = ''

    categories = os.listdir(SRCDIR)

    menu = ' '.join(sorted((f'--metadata="categories:{catname}"' for catname in categories)))
    context = {
        'menu': menu,
        'variables': { },
    }

    context['variables']['build_msg'] = build_msg
    # copy public files
    print(f'Copy public files -> {BUILDDIR}')
    shutil.copytree(PUBLICDIR, BUILDDIR, dirs_exist_ok=True)

    all_posts = []
    posts_bycat = {}
    posts_bytag = {}
    for cat in categories:
        catdir = os.path.join(SRCDIR, cat)
        posts = os.listdir(catdir)
        posts_bycat[cat] = []
        for fname in posts:
            f = os.path.join(catdir, fname)
            (name, ext) = os.path.splitext(fname)
            if ext != '.md' or name.startswith('.#'):
                continue
            # Get all metadata as json
            mdjson = subprocess.check_output(
                f'pandoc {f} --data-dir=. -t html --metadata-file=./metadata.yaml --template=metadata',
                shell=True,
            )
            post = json.loads(mdjson)
            url = '/{}/{}/{}.html'.format(post['date'], cat, name)
            outfile = BUILDDIR + url
            post['url'] = url
            post['infile'] = f
            outdir = os.path.dirname(outfile)
            os.makedirs(outdir, exist_ok=True)

            print(f'Build page -> {outfile}')

            # Add post to proper list
            posts_bycat[cat].append(post)
            for tag in post['tags']:
                posts_bytag.setdefault(tag, []).append(post)

            all_posts.append(post)
            context['title'] = post['title']
            context['variables']['category'] = cat
            options = get_pandoc_options(outfile, 'article', context)
            subprocess.Popen(f"pandoc {f} {options}", shell=True).wait()

    # Build category indexes
    for cat in posts_bycat:
        build_index('category', cat, posts_bycat[cat], context)

    # Build tag indexes
    for tag in posts_bytag:
        build_index('tag', tag, posts_bytag[tag], context)

    # Build home
    build_index('', 'index', all_posts, context)

    # Add rss
    build_rss_feed(all_posts)
