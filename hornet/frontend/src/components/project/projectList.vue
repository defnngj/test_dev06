<template>
  <div class="home">
    <div style="height: 50px; text-align: left; width: 100%">
      <el-button type="primary" @click="showDialog()">创建</el-button>
    </div>

    <div style="height: 700px">
      <div v-for="(item, index) in projectData" :key="index" class="text item">
        <el-col :span="7" class="project-card">
          <el-card style="width: 300px">
            <div slot="header" class="clearfix">
              <span>{{ item.name }}</span>
              <div style="float: right">
                <el-dropdown>
                  <span class="el-dropdown-link">
                    <i class="el-icon-setting"></i>
                  </span>
                  <el-dropdown-menu slot="dropdown">
                    <el-dropdown-item>
                      <el-button type="text" @click="showEdit(item.id)"
                        >编辑</el-button
                      >
                    </el-dropdown-item>
                    <el-dropdown-item>
                      <el-button type="text" @click="deleteProject(item.id)"
                        >删除</el-button
                      >
                    </el-dropdown-item>
                  </el-dropdown-menu>
                </el-dropdown>
              </div>
            </div>
            <!-- {{ item.image }} -->
            <img
              :src="item.image"
              class="image"
              style="height: 235px; width: 235px"
            />
          </el-card>
        </el-col>
      </div>
    </div>
    <div style="width: 100%; text-align: right">
      <el-pagination
        background
        @current-change="handleCurrentChange"
        layout="prev, pager, next"
        :page-size="req.size"
        :total="total"
      >
      </el-pagination>
    </div>

    <!-- 引入子组件 -->
    <projectDialog
      v-if="dialogFlag"
      :title="dialogTitle"
      :pid="currentPorjectId"
      @cancel="closeDialog"
    ></projectDialog>
  </div>
</template>

<script>
// @ is an alias to /src
import projectDialog from "@/components/project/projectDialog.vue"
import ProjectApi from "../../request/project"

export default {
  name: "Porject",
  components: {
    projectDialog,
  },
  data() {
    return {
      dialogFlag: false,
      dialogTitle: "create",
      currentPorjectId: "",
      projectData: [],
      req: {
        page: 1,
        size: 6,
      },
      total: 50,
    }
  },
  mounted() {
    this.initProjectList()
  },

  methods: {
    async initProjectList() {
      const resp = await ProjectApi.getProjects(this.req)
      if (resp.success === true) {
        // 处理图片路径
        for (let i = 0; i < resp.items.length; i++) {
          resp.items[i].image = "/static/images/" + resp.items[i].image
        }

        this.projectData = resp.items
        this.total = resp.total
        // this.$message.success("查询成功！")
      } else {
        this.$message.error("查询失败！")
      }
    },

    showDialog() {
      this.dialogTitle = "create"
      this.dialogFlag = true
    },

    closeDialog() {
      this.dialogFlag = false
      this.initProjectList()
    },

    // 跳转到第几页
    handleCurrentChange(val) {
      this.req.page = val
      this.initProjectList()
    },

    showEdit(id) {
      this.currentPorjectId = id
      this.dialogTitle = "edit"
      this.dialogFlag = true
    },

    // 删除项目
    async deleteProject(id) {
      const resp = await ProjectApi.deleteProject(id)
      if (resp.success === true) {
        this.initProjectList()
        this.$message.success("删除成功！")
      } else {
        this.$message.error("删除失败！")
      }
    },
  },
}
</script>
