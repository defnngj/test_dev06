<template>
  <div class="home">
    <div class="main-window">
      <div class="main-desc">
        <h2>接口测试平台</h2>
        <p>用于教学，包含项目管理、模块用例管理、任务执行、测试报告等功能</p>
      </div>
      <el-tabs v-model="activeName" type="border-card" class="login-window">
        <el-tab-pane label="登录" name="first">
          <el-form
            :model="loginForm"
            :rules="rules"
            ref="loginForm"
            label-position="left"
            label-width="100px"
          >
            <el-form-item label="用户" prop="username">
              <el-input
                v-model="loginForm.username"
                cy-data="LoginUsername"
              ></el-input>
            </el-form-item>
            <el-form-item label="密码" prop="password">
              <el-input
                v-model="loginForm.password"
                type="password"
                cy-data="LoginPassword"
              ></el-input>
            </el-form-item>
            <el-form-item>
              <el-button
                type="primary"
                @click="submitLogin('loginForm')"
                style="width: 270px"
                cy-data="loginButton"
                >登录</el-button
              >
            </el-form-item>
          </el-form>
        </el-tab-pane>
        <el-tab-pane label="注册" name="second">
          <el-form
            :model="registerForm"
            :rules="rules"
            ref="registerForm"
            label-position="left"
            label-width="100px"
          >
            <el-form-item label="用户" prop="username">
              <el-input
                v-model="registerForm.username"
                cy-data="username"
              ></el-input>
            </el-form-item>
            <el-form-item label="设置密码" prop="password">
              <el-input
                v-model="registerForm.password"
                type="password"
                cy-data="password"
              ></el-input>
            </el-form-item>
            <el-form-item label="确认密码" prop="confirm_password">
              <el-input
                v-model="registerForm.confirm_password"
                type="password"
              ></el-input>
            </el-form-item>
            <el-form-item>
              <el-button
                type="success"
                @click="submitRegister('registerForm')"
                style="width: 270px"
                >注册</el-button
              >
            </el-form-item>
          </el-form>
        </el-tab-pane>
      </el-tabs>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
// import HelloWorld from "@/components/HelloWorld.vue";
import UserApi from "../request/user"

export default {
  name: "Home",
  components: {
    // HelloWorld,
  },
  data() {
    return {
      activeName: "first",
      loginForm: {
        username: "tom",
        password: "tom123456",
      },
      registerForm: {
        username: "",
        password: "",
        confirm_password: "",
      },
      rules: {
        username: [{ required: true, message: "请输入用户", trigger: "blur" }],
        password: [{ required: true, message: "请输入密码", trigger: "blur" }],
        confirm_password: [
          { required: true, message: "请输入确认密码", trigger: "blur" },
        ],
      },
    }
  },
  methods: {
    // 用户登录
    submitLogin(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          // alert('submit!');
          UserApi.login(this.loginForm).then((resp) => {
            if (resp.success === true) {
              sessionStorage.token = resp.item.token
              sessionStorage.user = resp.item.username
              // this.$store.commit('login', resp.data.Token)
              this.$router.push({ path: "/main" })
              this.$message.success("登录成功！")
            } else {
              this.$message.error(resp.error.message)
            }
          })
        } else {
          return false
        }
      })
    },

    // 用户注册
    submitRegister(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          // alert('submit!');
          UserApi.register(this.registerForm).then((resp) => {
            if (resp.success === true) {
              this.$message.success("注册成功！")
            } else {
              this.$message.error(resp.error.message)
            }
          })
        } else {
          return false
        }
      })
    },
  },
}
</script>

<style scoped>
.main-window {
  text-align: center;
  margin: 0 auto;
  width: 800px;
  margin-top: 200px;
}
.main-desc {
  width: 350px;
  float: left;
}
.login-window {
  width: 400px;
  float: right;
}
</style>
