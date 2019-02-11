const path = require("path");

const config = {
    entry: ["./react/index.tsx"],
    mode: "development",
    output: {
        path: path.resolve(__dirname, "static/build"),
        filename: "bundle.js"
    },
    resolve: {
        extensions: [".ts", ".tsx", ".js", ".jsx"]
    },
    module: {
        rules: [
            {
                test: /\.tsx?$/,
                use: ['ts-loader']
            },
            {
                test: /\.css$/,
                use: ['style-loader', 'css-loader']
            }
        ]
    }
};

module.exports = config;