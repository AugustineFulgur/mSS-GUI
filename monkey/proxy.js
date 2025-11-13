(function() {{
    // 这个不是monkey脚本，是给mi_webpack.Ctx_proxypack用的
    // 0 变量原名 1 app.js（_hex） 2 原始赋值语句
    if (!window.{1}) {{
        window.{1} = {{}};
    }}
    window.{1}.{0}={{}};

    const targetObject = {{
        value: {2}
    }};

    const handler = {{
        get: function(t, p) {{

            window.{1}.{0}[p] = t[p];
            return t[p];
        }},
        set: function(t, p, v) {{
            t[p] = v;
            window.{1}.{0}[p] = v;
            return true;
        }}
    }};

    const proxy = new Proxy(targetObject, handler);
    return proxy;
}})();