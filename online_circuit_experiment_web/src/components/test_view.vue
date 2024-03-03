<template>
  <el-form ref="form" :model="form" :rules="rules" label-width="100px">
    <el-form-item label="age" prop="age">
      <el-input v-model.number="form.age" type="age"></el-input>
    </el-form-item>
  </el-form>
</template>

<script>
const checkAge = (rule, value, callback) => {
  console.warn('checkAge');
  if (value < 18) {
    callback(new Error('Age must be greater than 18'));
  } else {
    callback();
  }
};
export default {
  name: "test_view",
  data() {
    // const checkAge = (rule, value, callback) => {
    //     console.warn('checkAge');
    //     if (value < 18) {
    //         callback(new Error('Age must be greater than 18'));
    //     } else {
    //         callback();
    //     }
    // };
    return {
      form: {
        age: ''
      },
      rules: {
        age: [
          { required: true, message: 'age is required' },
          { type: 'number', message: 'age must be a number' },
          { validator: checkAge, trigger: ['blur', 'change'] }
        ]
      }
    };
  }
};
</script>
