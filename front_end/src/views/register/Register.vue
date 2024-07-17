<template>
  <div>
    <el-card class="box-card">
      <h2>注册</h2>
      <el-form :model="ruleForm" status-icon :rules="rules" ref="ruleForm" label-position="left" label-width="80px"
        class="demo-ruleForm">
        <el-form-item label="用户名" prop="uname">
          <el-input v-model="ruleForm.uname"></el-input>
        </el-form-item>
        <el-form-item label="密码" prop="pass">
          <el-input type="password" v-model="ruleForm.pass" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="确认密码" prop="password">
          <el-input type="password" v-model="ruleForm.password" autocomplete="off"></el-input>
        </el-form-item>
      </el-form>
      <div class="btnGroup">
        <el-button type="primary" @click="submitForm('ruleForm')" v-loading="loading">提交</el-button>
        <el-button @click="resetForm('ruleForm')">重置</el-button>
        <el-button @click="goBack">返回</el-button>
      </div>
    </el-card>
  </div>
</template>

<script>
import axiosInstance from '@/utils/axiosInstance';
import qs from 'qs';

export default {
  data() {
    var validatePass = (rule, value, callback) => {
      if (value === "") {
        callback(new Error("请输入密码"));
      } else {
        if (this.ruleForm.checkPass !== "") {
          this.$refs.ruleForm.validateField("checkPass");
        }
        callback();
      }
    };
    var validatePass2 = (rule, value, callback) => {
      if (value === "") {
        callback(new Error("请再次输入密码"));
      } else if (value !== this.ruleForm.pass) {
        callback(new Error("两次输入密码不一致!"));
      } else {
        callback();
      }
    };
    return {
      ruleForm: {
        uname: "",
        pass: "",
        password: "",
      },
      rules: {
        uname: [
          { required: true, message: "用户名不能为空！", trigger: "blur" },
        ],
        pass: [{ required: true, validator: validatePass, trigger: "blur" }],
        password: [
          { required: true, validator: validatePass2, trigger: "blur" },
        ],
      },
      loading: false
    };
  },
  methods: {
    submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.loading = true;  // 提交按钮显示加载动画
          console.log('Sending register request with data:', this.ruleForm); // 打印发送的数据
          
          axiosInstance.post('/user/register', qs.stringify({
            uname: this.ruleForm.uname,
            password: this.ruleForm.password
          }))
            .then((res) => {
              this.loading = false;
              const responseData = res.data;
              console.log('Response data:', responseData);
              if (responseData.code === 0) {
                this.$router.push('/login');
                this.$message({
                  message: responseData.msg,
                  type: "success",
                });
              } else {
                this.$message({
                  message: responseData.msg,
                  type: "warning",
                });
              }
            })
            .catch(error => {
              this.loading = false;
              this.$message({
                message: '注册失败，请重试。',
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
    goBack() {
      this.$router.go(-1);
    },
    created() {
      // 初始化逻辑
    }
  }
};
</script>

<style scoped>
/* 设置登录面板居中，宽度为400px */
.box-card {
  margin: auto auto;
  width: 400px;
}

/* 设置登录面板中的表单居中 */
.login-from {
  margin: auto auto;
}
</style>