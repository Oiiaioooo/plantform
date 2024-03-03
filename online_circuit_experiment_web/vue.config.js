// module.exports={
//     devServer: {
//         host: '0.0.0.0',
//         port: 8080, // 你可以选择任何喜欢的端口
//         // publicPath:'/', // 和 publicPath 保持一致
//
//     }
// }
module.exports = {
    devServer: {
        host: '0.0.0.0',
        port: 8081, // 你可以选择其他端口
        // proxy: {
        //     '/api': {
        //         target: 'http://127.0.0.1:8000',
        //         changeOrigin: true,
        //     },
        // },
    },

};
