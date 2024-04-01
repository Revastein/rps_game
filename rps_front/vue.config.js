const { defineConfig } = require('@vue/cli-service');

module.exports = defineConfig({
  transpileDependencies: true,
  chainWebpack: (config) => {
    config.plugin('define').tap((args) => {
      const flags = args[0] || {};
      flags['__VUE_PROD_HYDRATION_MISMATCH_DETAILS__'] = false;
      return [flags];
    });
  },
});
