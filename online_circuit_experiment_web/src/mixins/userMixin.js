export default {
  methods: {
    getCurrentUser() {
      return new Promise((resolve, reject) => {
        this.$get('/users/me').then(response => {
          resolve(response)
        }).catch(error => {
          if (error.response && error.response.status === 401) {
            sessionStorage.removeItem('token');
            this.$router.push('/');
          }
          reject(error);
        });
      });
    }
  }
}