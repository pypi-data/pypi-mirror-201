
try {
    new Function("import('/reactfiles/frontend/main.ec45ccd0.js')")();
} catch (err) {
    var el = document.createElement('script');
    el.src = '/reactfiles/frontend/main.ec45ccd0.js';
    el.type = 'module';
    document.body.appendChild(el);
}
