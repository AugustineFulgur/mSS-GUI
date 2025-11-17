var {0}=(function() {{
    // 这个不是monkey脚本，是给mi_webpack.Ctx_proxypack用的
    // 0 变量原名 1 原始赋值语句
    window.__mss__.{0}={{}};

    const targetObject = {{
        value: {1}
    }};

    const handler = {{
        get: function(t, p) {{

            window.__mss__.{0}[p] = t[p];
            return t[p];
        }},
        set: function(t, p, v) {{
            t[p] = v;
            window.__mss__.{0}[p] = v;
            return true;
        }}
    }};

    const proxy = new Proxy(targetObject, handler);
    return proxy;
}})();