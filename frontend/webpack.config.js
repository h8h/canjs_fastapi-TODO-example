const path = require("path");
const UglifyJSPlugin = require("uglifyjs-webpack-plugin");
const webpack = require("webpack");
const MiniCssExtractPlugin = require('mini-css-extract-plugin');

module.exports = {
  entry: "./index.js",
  output: {
    filename: "bundle.js",
    path: path.resolve(__dirname, "dist", "dist")
  },
  mode: "development",
  module: {
   rules: [
      {
        exclude: /node_modules/,
        test: /\.(js)$/,
        use: ["babel-loader"]
      },
      {
        test: /\.stache$/,
        use: {
          loader: "can-stache-loader"
        }
      },
      {
        test: /\.less$/i,
         use: [
          {
            loader: MiniCssExtractPlugin.loader,
          },
          {
            loader: "css-loader",
          },
          {
            loader: "less-loader",
            options: {
              lessOptions: {
                strictMath: true,
              },
            },
          },
        ],
      },
    ]
  },
  plugins: [
    new MiniCssExtractPlugin(),
    new webpack.optimize.SideEffectsFlagPlugin(),
    new UglifyJSPlugin({
        sourceMap: true,
        uglifyOptions: { compress: false, mangle: false, dead_code: true }
    })
  ],
  devtool: 'source-map',
  resolve: {
    extensions: ["*", ".js"]
  }
};
