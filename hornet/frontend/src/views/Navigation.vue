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
          <router-link to="/main/about">
            <el-menu-item index="1" class="menu-option">
              <i class="el-icon-s-home"></i>
              <template #title> About</template>
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
          <span>欢迎~ {{ user }}</span>
        </el-header>

        <el-main style="background-color: #f1f3fa">
          <router-view> </router-view>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>
export default {
  data() {
    return {
      user: "",
    };
  },
  created() {
    this.user = sessionStorage.getItem("user");
  },

  methods: {},
};
</script>

<style>
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
