// 获取vue-router 给插件用的 带proxy的都是给插件用的 谢谢 当然你也可以直接使用 它会输出当前router
// 你可以随时使用window.__mss__.routers 来获取当前注册的所有路由

if(!window.__mss__){window.__mss__={};}
window.__mss__.routers=[]; 

function turtle(node,re,rpath=""){ //递归 
    //写得头疼讨厌死了
    if(!node.children){
        re.push(rpath+node.path);
        return; //当没有子节点的时候返回
    } 
    node.children.forEach(c=>{
        turtle(c,re,rpath); //对所有子节点调用
    })
    return;
}

var routes=null;

if(document.querySelector("#app").__vue__){
    //vue 2
    routes=document.querySelector("#app").__vue__.$router;
    document.querySelector("#app").__vue__.$router=new Proxy(routes,{
        get(t,p){
            if(p==="addRoute"){
                return function (...args){
                    var parent=args.length===1?'':args[0]; //在这个语言整花活许多时候会招致不幸
                    var r=[args[-1].path]
                    var re=[];
                    turtle([args[-1].path],re,args.length===1?'':args[0]);
                    window.__mss__.routers.push(re);
                    return routes.apply(this,args)
                }
            }
        }
    })
}else{
    //vue 3
    routes=document.querySelector("#app").__vue_app__.config.globalProperties.$router;
    document.querySelector("#app").__vue_app__.config.globalProperties.$router=new Proxy(routes,{
        get(t,p){
            if(p==="addRoute"){
                return function (...args){
                    var parent=args.length===1?'':args[0]; //在这个语言整花活许多时候会招致不幸
                    var r=[args[-1].path]
                    for (i of args[-1].children){
                        r.push(r[0]+i.path); 
                    }
                    window.__mss__.routers.push(r);
                    return routes.apply(this,args)
                }
            }
        }
    })
}
re=[];
routes.options.routes.forEach(e=>{turtle(e,re,'');});
window.__mss__.routers.push(re);

// 调试语句
console.log("初始化路由："+re);



