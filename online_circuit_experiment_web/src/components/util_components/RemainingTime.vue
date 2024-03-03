<template>
  <div class="remaining-time-container">
    <el-row>
      <el-col :span="18">
        <el-tag type="warning" class="time-tag">{{ remainingTime }}</el-tag>
      </el-col>
      <el-col :span="6">
      </el-col>
    </el-row>
  </div>
</template>

<script>

import userMixin from '@/mixins/userMixin.js';
export default {
  name: 'RemainingTime',
  components: {
  },
  data() {
    return {
      valid_until: null,
      remainingTime: ''
    };
  },
  mixins: [userMixin],
  created() {
    this.getCurrentUser().then(response => {
      this.valid_until = response.valid_until;
      this.calculateRemainingTime();
      setInterval(this.calculateRemainingTime, 1000); // Update every second
    }).catch(error => {
      console.error("Failed to get user information:", error);
    });
  },
  methods: {
    calculateRemainingTime() {
      if (this.valid_until) {
        const now = new Date();
        const validUntil = new Date(this.valid_until);
        const diff = validUntil - now;
        if (diff > 0) {
          const diffHours = Math.floor(diff / (1000 * 60 * 60));
          const diffMinutes = Math.floor((diff / (1000 * 60)) % 60);
          const diffSeconds = Math.floor((diff / 1000) % 60);
          this.remainingTime = `剩余时间 ${diffHours}:${diffMinutes}:${diffSeconds}`;
        } else {
          this.remainingTime = 'Expired';
        }
      }
    }
  }
};
</script>
<style scoped>
.remaining-time-container {
  margin-bottom: 20px;
}

.time-tag {
  font-size: 16px;
  line-height: 2;
}
</style>
