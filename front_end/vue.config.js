module.exports = {
    lintOnSave: false, // 关闭语法检测
    devServer: {
      proxy: {
        '/api': {
          target: 'http://47.113.222.46:8081',
          ws: true, // 是否启用websockets
          changeOrigin: true,  // 代理时是否更改host
          pathRewrite: {
            '^/api': '' // 这里理解成用'/api'代替target里面的地址
          },
          onProxyReq: (proxyReq, req, res) => {
            // 手动设置 Authorization 请求头
            const token = req.headers.authorization;
            if (token) {
              proxyReq.setHeader('Authorization', token);
            }
          }
        }
      }
    }
  }
  