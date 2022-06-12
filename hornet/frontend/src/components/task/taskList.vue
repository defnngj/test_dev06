<template>
  <div class="home">
    <div style="text-align: left">
      <el-form :inline="true" :model="projectForm" class="demo-form-inline">
        <el-form-item label="项目">
          <el-select v-model="projectForm.id" placeholder="请选择项目">
            <el-option
              v-for="item in projectOption"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            >
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="createTask()">创建</el-button>
        </el-form-item>
      </el-form>
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
    <taskDialog
      v-if="dialogFlag"
      :title="dialogTitle"
      :pid="projectForm.id"
      @cancel="closeDialog"
    ></taskDialog>
  </div>
</template>

<script>
// @ is an alias to /src
import taskDialog from "@/components/task/taskDialog.vue"
import ProjectApi from "../../request/project"

export default {
  name: "Porject",
  components: {
    taskDialog,
  },
  data() {
    return {
      projectForm: {
        id: "",
      },
      projectOption: [],
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
    console.log("mounted11")
    this.initProjectList()
  },

  methods: {
    // 初始化项目列表
    async initProjectList() {
      const resp = await ProjectApi.getProjects(this.req)
      if (resp.success === true) {
        this.projectValue = resp.items[0].id
        this.projectLabel = resp.items[0].name

        for (let i = 0; i < resp.items.length; i++) {
          this.projectOption.push({
            value: resp.items[i].id,
            label: resp.items[i].name,
          })
        }

        // this.$message.success("查询成功！")
      } else {
        this.$message.error("查询失败！")
      }
    },

    onSubmit() {
      console.log("submit!")
    },

    createTask() {
      this.dialogTitle = "create"
      this.dialogFlag = true
    },

    closeDialog() {
      this.dialogFlag = false
      this.initProjectList()
    },

    // 跳转到第几页
    handleCurrentChange(val) {
      console.log(`当前页: ${val}`)
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
