const ANSI = {
  green: '\x1b[32m',   
  bold: '\x1b[1m',      
  reset: '\x1b[0m'      
};

console.log(``);

console.log(`hello ${ANSI.green}${ANSI.bold}monkey-mSS!${ANSI.reset}`);
console.log("猴子脚本运行中");