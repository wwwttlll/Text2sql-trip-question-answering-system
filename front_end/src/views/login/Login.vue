<template>
  <div>
    <el-card class="box-card">
      <h2>登录</h2>
      <el-form :model="ruleForm" status-icon :rules="rules" ref="ruleForm" label-position="left" label-width="70px"
        class="login-from">
        <el-form-item label="用户名" prop="uname">
          <el-input v-model="ruleForm.uname"></el-input>
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input type="password" v-model="ruleForm.password" autocomplete="off"></el-input>
        </el-form-item>
      </el-form>
      <div class="btnGroup">
        <el-button type="primary" @click="submitForm('ruleForm')" v-loading="loading">登录</el-button>
        <el-button @click="resetForm('ruleForm')">重置</el-button>
        <router-link to="/register">
          <el-button style="margin-left: 10px">注册</el-button>
        </router-link>
      </div>
    </el-card>
  </div>
</template>

<script>
import axiosInstance from '@/utils/axiosInstance';
import MockAdapter from 'axios-mock-adapter';
import qs from 'qs';

export default {
  data() {
    return {
      ruleForm: {
        uname: "",
        password: "",
      },
      rules: {
        uname: [
          { required: true, message: "用户名不能为空！", trigger: "blur" },
        ],
        password: [
          { required: true, message: "密码不能为空！", trigger: "blur" },
        ],
      },
      loading: false,
    };
  },
  methods: {
    submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.loading = true;
          console.log('Sending login request with data:', this.ruleForm); // 打印发送的数据
          /*
                    // 模拟后端响应
                    const mock = new MockAdapter(axiosInstance);
                    mock.onPost('/api/user/login').reply(200, {
                      code: 0,
                      msg: '登录成功',
                      data: 'mockedToken',
                    });
          */
          axiosInstance.post('/user/login', qs.stringify({
            uname: this.ruleForm.uname,
            password: this.ruleForm.password
          }))
            .then((res) => {
              this.loading = false;
              const responseData = res.data;
              console.log('Response data:', responseData);
              if (responseData.code === 0) {
                const token = responseData.data;
                sessionStorage.setItem("token", token);
                console.log(token);
                this.$router.push('/home');
                this.$message({
                  message: responseData.msg,
                  type: "success",
                });
              } else {
                this.$message({
                  message: responseData.msg,
                  type: "error",
                });
              }
            })
            .catch(error => {
              this.loading = false;
              this.$message({
                message: '登录失败，请检查用户名或密码。',
                type: 'error',
              });
              console.error('Request failed with status:', error.response.status);
              console.error('Request failed with message:', error.response.data);
            });
        } else {
          console.log("error submit!!");
        }
      });
    },
    resetForm(formName) {
      this.$refs[formName].resetFields();
    },
  },
  created() {

  },
};
</script>

<style scoped>
.box-card {
  margin: auto auto;
  width: 400px;
}

.login-from {
  margin: auto auto;
}
</style>
