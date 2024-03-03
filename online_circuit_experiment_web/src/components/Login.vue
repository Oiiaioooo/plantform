<template>
  <div class="login-container">
    <el-card class="login-card">
      <div class="login-header">
        <h3>远程实验系统登录</h3>
      </div>
      <el-form @submit.native.prevent="login">
        <el-form-item>
          <el-input v-model="username" placeholder="Username" prefix-icon="el-icon-user"></el-input>
        </el-form-item>
        <el-form-item>
          <el-input v-model="password" type="password" placeholder="Password" prefix-icon="el-icon-lock"></el-input>
        </el-form-item>
        <el-form-item class="form-button">
          <el-button type="primary" native-type="submit">登录</el-button>
        </el-form-item>
      </el-form>
      <div v-if="user">
        User {{ user.username }} successfully logged in as {{ user.role }}
      </div>
    </el-card>
  </div>
</template>

<script>
import userMixin from '@/mixins/userMixin.js';

export default {
  data() {
    return {
      username: '',
      password: '',
      user: null
    };
  },
  mixins: [userMixin],
  methods: {
    // ... 保持原有的 login 方法不变 ...
    login() {
      const formData = new URLSearchParams();
      formData.append('username', this.username);
      formData.append('password', this.password);

      this.$post('/token', formData)
          .then(response => {
            console.log(response); // 添加这行来查看响应内容
            const token = response.access_token;
            console.log("Token received:", token);
            sessionStorage.setItem('token', token);
            this.getCurrentUser().then(response=>{
              this.user=response
              console.log('getCurrentUser',this.user)
              sessionStorage.setItem('user',JSON.stringify(response))
            })
            this.$router.push('/dashboard')
            // 其他操作...
          }).catch(error => {
        console.error(error);
        alert('Login failed!');
      });
    }
  }
};
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

.login-card {
  width: 400px;
}

.login-header {
  text-align: center;
  margin-bottom: 20px;
}

.form-button {
  text-align: center; /* 添加这行来居中按钮 */
}
</style>
