<template>
  <div class="navigation">
    <el-container style="height: 100%; border: 1px solid #eee">
      <el-aside width="200px" style="background-color: #343a40">
        <img class="logo" alt="itest logo" src="../assets/logo.svg" />
        <el-menu
          default-active="onRoutes"
          class="el-menu-vertical-demo"
          background-color="#343a40"
          text-color="#fff"
          active-text-color="#ffd04b"
        >
          <router-link to="/main/project">
            <el-menu-item index="1" class="menu-option">
              <i class="el-icon-menu"></i>
              <template #title>项目管理</template>
            </el-menu-item>
          </router-link>
          <router-link to="/main/case">
            <el-menu-item index="2" class="menu-option">
              <i class="el-icon-s-grid"></i>
              <template #title>用例管理</template>
            </el-menu-item>
          </router-link>
          <router-link to="/main/task">
            <el-menu-item index="3" class="menu-option">
              <i class="el-icon-s-order"></i>
              <template #title>任务管理</template>
            </el-menu-item>
          </router-link>
          <router-link to="/main/report">
            <el-menu-item index="4" class="menu-option">
              <i class="el-icon-document-copy"></i>
              <template #title>报告管理</template>
            </el-menu-item>
          </router-link>
          <router-link to="/main/extract">
            <el-menu-item index="5" class="menu-option">
              <i class="el-icon-s-operation"></i>
              <template #title>变量管理</template>
            </el-menu-item>
          </router-link>
          <router-link to="/main/performance">
            <el-menu-item index="6" class="menu-option">
              <i class="el-icon-odometer"></i>
              <template #title>性能管理</template>
            </el-menu-item>
          </router-link>
        </el-menu>
      </el-aside>

      <el-container>
        <el-header style="text-align: right; font-size: 12px">
          <el-dropdown>
            <i class="el-icon-setting" style="margin-right: 15px"></i>
            <el-dropdown-menu slot="dropdown">
              <el-dropdown-item>查看</el-dropdown-item>
              <el-dropdown-item>新增</el-dropdown-item>
              <el-dropdown-item>删除</el-dropdown-item>
            </el-dropdown-menu>
          </el-dropdown>
          <span cy-data="loginSuccess">欢迎~ {{ user }}</span>
        </el-header>

        <el-main style="background-color: #f1f3fa">
          <el-card style="min-height: 800px">
            <router-view> </router-view>
          </el-card>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>
export default {
  computed: {
    onRoutes() {
      if (this.$route.path === "/main/project") {
        return "1"
      } else if (this.$route.path === "/main/case") {
        return "2"
      } else if (this.$route.path === "/main/task") {
        return "3"
      } else if (this.$route.path === "/main/report") {
        return "4"
      } else if (this.$route.path === "/main/extract") {
        return "5"
      } else if (this.$route.path === "/main/performance") {
        return "5"
      }
      return "1"
    },
  },
  data() {
    return {
      user: "",
    }
  },
  created() {
    this.user = sessionStorage.getItem("user")
  },

  methods: {},
}
</script>

<style scoped>
.navigation {
  height: 100%;
}

.nav {
  height: 100%;
}
.el-container {
  height: 100%;
}

a {
  text-decoration: none;
}

.router-link-active {
  text-decoration: none;
}

.logo {
  margin-top: 20px;
  margin-bottom: 10px;
  height: 22px;
}
.el-header {
  color: #343a40;
  line-height: 60px;
}

.el-aside {
  color: #343a40;
}
</style>
