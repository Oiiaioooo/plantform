<template>
  <el-button @click="logout" type="danger">Logout</el-button>
</template>

<script>
export default {
  methods: {
    logout() {
      this.$post('/logout')
          .then(() => {
            sessionStorage.removeItem('token');
            this.$router.push('/');
          })
          .catch(error => {
            console.error("Failed to logout:", error);
          });
    }
  }
};
</script>

<style scoped>
/* 可以添加一些自定义样式，如果需要 */
</style>
