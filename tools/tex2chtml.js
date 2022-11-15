const process = require('process');
const fs = require('fs');
//const mathjax = require('mathjax-full');

const {mathjax} = require('mathjax-full/js/mathjax.js');
const {TeX} = require('mathjax-full/js/input/tex.js');
const {CHTML} = require('mathjax-full/js/output/chtml.js');
const {liteAdaptor} = require('mathjax-full/js/adaptors/liteAdaptor.js');
const {RegisterHTMLHandler} = require('mathjax-full/js/handlers/html.js');
const {AssistiveMmlHandler} = require('mathjax-full/js/a11y/assistive-mml.js');

const {AllPackages} = require('mathjax-full/js/input/tex/AllPackages.js');

require('mathjax-full/js/util/entities/all.js');

const CONFIG = {
    em: 16,
    ex: 8,
    fontURL: '/fonts/mathjax',
};

const inputFile = fs.readFileSync(process.argv[2], 'utf8');
const outputFilename = process.argv[3];

const adaptor = liteAdaptor({ fontSize: CONFIG.em });
AssistiveMmlHandler(RegisterHTMLHandler(adaptor));

const tex = new TeX({ packages: AllPackages.sort(), inlineMath: [['$','$']], tags: 'ams' });
const chtml = new CHTML({ fontURL: CONFIG.fontURL, exFactor: CONFIG.ex / CONFIG.em, displayAlign: 'left' });
const html = mathjax.document(inputFile, { InputJax: tex, OutputJax: chtml });

html.render();

if (Array.from(html.math).length === 0) {
    adaptor.remove(html.outputJax.chtmlStyles);
}

const outputContent = adaptor.doctype(html.document) + '\n' + adaptor.outerHTML(adaptor.root(html.document));
fs.writeFileSync(outputFilename, outputContent, { encoding: 'utf-8' });


/* MathJax.init({
 *     loader: {
 *         source: require('mathjax-full/components/src/source.js').source,
 *         load: ['adaptors/liteDOM', 'tex-chtml'],
 *     },
 *     tex: {
 *         packages: CONFIG.packages,
 *         tags: 'ams',
 *     },
 *     chtml: {
 *         fontURL: CONFIG.fontURL,
 *         exFactor: CONFIG.ex / CONFIG.em,
 *         displayAlign: 'left',
 *     },
 *     'adaptors/liteDOM': {
 *         fontSize: CONFIG.em,
 *     },
 *     startup: {
 *         document: inputFile,
 *     },
 * })
 *     .then((MathJax) => {
 *         const adaptor = MathJax.startup.adaptor;
 *         const html = MathJax.startup.document;
 *         if (Array.from(html.math).length === 0) {
 *             adaptor.remove(html.outputJax.chtmlStyles);
 *         }
 * 
 *         const outputContent = adaptor.doctype(html.document) + '\n' + adaptor.outerHTML(adaptor.root(html.document));
 *         fs.writeFileSync(outputFilename, outputContent, { encoding: 'utf-8' });
 *     })
 *     .catch(err => console.error(err)); */
