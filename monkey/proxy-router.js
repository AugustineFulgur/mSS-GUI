// 0 appname 1 loaderkey 2 router
function monkey_getloader() { //工具函数，获取当前加载器
  for (const [key, value] of Object.entries(window.__mss__)) {
    if (value && '{1}' in value) {
      console.log(key); 
      return key; 
    }
  }
}

