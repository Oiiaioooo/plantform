<template>
  <el-container class="dashboard-container">
    <el-header class="dashboard-header">
      <div class="header-content">
        <h1 class="welcome-text">欢迎, {{ username }}</h1>
        <div class="header-right">
          <RemainingTime />
          <Logout />
        </div>
      </div>
    </el-header>
    <el-main>
      <div class="button-container">
        <el-button type="primary" @click="goToExp">进入实验</el-button>
        <el-button v-if="isAdmin" type="success" @click="goToExp_Management">进入实验管理</el-button>
      </div>
    </el-main>
  </el-container>
</template>
<script>
import RemainingTime from './util_components/RemainingTime.vue';
import userMixin from '@/mixins/userMixin.js';
import Logout from './util_components/Logout.vue';
export default {
  name: 'Dashboard',
  components: {
    RemainingTime,
    Logout
  },
  data() {
    return {
      username: '', // 假设用户名，您可以根据需要调整
      role: '' // 假设用户角色，您可以根据需要调整
    };
  },
  mixins: [userMixin],
  created() {
    this.getCurrentUser().then(response => {
      this.username = response.username; // 设置用户名
      this.role = response.role; // 设置用户角色
    }).catch(error => {
      console.error("获取用户信息失败:", error);
      // 可以根据错误进行进一步处理，如重定向到登录页面
    });
  },
  computed: {
    isAdmin() {
      return this.role === 'admin'; // 判断用户是否是管理员
    }
  },
  methods: {
    goToExp() {
      this.$router.push('/exp'); // 导航到实验页面
    },
    goToExp_Management() {
      this.$router.push('/exp_management'); // 导航到实验管理页面
    }
  }
};
</script>



<style scoped>
.dashboard-container {
  text-align: center;
}

.dashboard-header {
  background-color: #409EFF;
  color: white;
  padding: 10px 30px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.welcome-text {
  margin: 0;
  font-size: 24px;
}

.header-right {
  display: flex;
  align-items: center;
}

.el-main {
  display: flex;
  justify-content: center;
  align-items: center;
  height: calc(100vh - 60px); /* Adjust the height based on your header height */
}

.button-container {
  text-align: center;
}

/* Add additional styles if needed */
</style>
