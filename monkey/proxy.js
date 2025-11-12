// 这个不是monkey脚本，是给mi_webpack.Ctx_proxypack用的
// 0 变量原名 1 app.js（_hex） 2 原始赋值语句

if(!window.{1}) window.{1}={{}};

{0} = new Proxy({0},{{
    get(t,p){{
        window.{1}.{0}[p]=t[p];
        return t[p];
    }},
    set(t,p,v){{
        t[p]=v;
        window.{1}.{0}[p]=v;
        return true;
    }}
}});

window.{1}.{0}={2}