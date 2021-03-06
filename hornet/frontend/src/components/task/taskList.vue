<template>
  <div class="home">
    <div style="text-align: left">
      <el-form :inline="true" :model="projectForm">
        <el-form-item label="项目">
          <el-select
            v-model="projectForm.id"
            size="medium"
            placeholder="请选择项目"
          >
            <el-option
              v-for="item in projectOption"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            >
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item style="float: right">
          <el-button type="primary" size="medium" @click="createTask()"
            >创建任务</el-button
          >
        </el-form-item>
      </el-form>
    </div>

    <div>
      <el-table :data="taskData" border style="width: 100%">
        <el-table-column prop="id" label="ID" width="80"> </el-table-column>
        <el-table-column prop="name" label="名称"> </el-table-column>
        <el-table-column prop="describe" label="描述"> </el-table-column>
        <el-table-column prop="create_time" label="创建"> </el-table-column>
        <el-table-column prop="update_time" label="更新"> </el-table-column>
        <el-table-column prop="status" label="状态">
          <template slot-scope="scope">
            <div v-if="scope.row.status === 0">
              <el-tag type="info"> 未执行</el-tag>
            </div>
            <div v-else-if="scope.row.status === 1">
              <el-tag type="success"> 执行中</el-tag>
            </div>
            <div v-else-if="scope.row.status === 2">
              <el-tag> 已执行</el-tag>
            </div>
            <div v-else>
              <el-tag type="danger"> 未知 </el-tag>
            </div>
          </template>
        </el-table-column>
        <el-table-column fixed="right" label="操作" width="150">
          <template slot-scope="scope">
            <el-button @click="runTask(scope.row)" type="text" size="small"
              >执行</el-button
            >
            <el-button @click="showCase(scope.row)" type="text" size="small"
              >顺序</el-button
            >
            <el-button type="text" size="small" @click="editTask(scope.row)"
              >编辑</el-button
            >
            <el-button type="text" size="small" @click="deleteTask(scope.row)"
              >删除</el-button
            >
          </template>
        </el-table-column>
      </el-table>
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
      :tid="taskId"
      @cancel="closeDialog"
    ></taskDialog>
    <taskCase
      v-if="caseFlag"
      :pid="projectForm.id"
      :tid="taskId"
      @cancel="closeDialog"
    >
    </taskCase>
  </div>
</template>

<script>
// @ is an alias to /src
import taskDialog from "@/components/task/taskDialog.vue"
import taskCase from "@/components/task/taskCase.vue"
import ProjectApi from "../../request/project"
import TaskApi from "../../request/task"

export default {
  name: "Porject",
  components: {
    taskDialog,
    taskCase,
  },
  data() {
    return {
      projectForm: {
        id: 1,
      },
      projectOption: [],
      dialogFlag: false,
      dialogTitle: "create",
      currentPorjectId: "",
      taskId: "",
      projectData: [],
      req: {
        page: 1,
        size: 6,
      },
      total: 50,
      taskData: [],
      taskHeartbeat: null,
      caseFlag: false,
    }
  },
  mounted() {
    this.initProjectList()
    this.taskHeartbeat = setInterval(() => {
      this.initTaskList()
    }, 5000)
  },
  destroyed() {
    // 销毁时候清除定时器
    clearInterval(this.taskHeartbeat)
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
        this.initTaskList()
        // this.$message.success("查询成功！")
      } else {
        this.$message.error("查询失败！")
      }
    },
    // 初始化任务列表
    async initTaskList() {
      const req = { project_id: this.projectForm.id }
      const resp = await TaskApi.getTaskList(req)
      if (resp.success === true) {
        this.taskData = resp.items
        // this.$message.success("查询成功！")
      } else {
        this.$message.error("查询失败！")
      }
    },

    createTask() {
      this.dialogTitle = "create"
      this.dialogFlag = true
    },

    editTask(row) {
      this.dialogTitle = "edit"
      this.taskId = row.id
      this.dialogFlag = true
    },

    showCase(row) {
      this.taskId = row.id
      this.caseFlag = true
    },

    closeDialog() {
      this.dialogFlag = false
      this.caseFlag = false
      // this.initProjectList()
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
    async deleteTask(row) {
      const resp = await TaskApi.deleteTask(row.id)
      if (resp.success === true) {
        this.initProjectList()
        this.$message.success("删除成功！")
      } else {
        this.$message.error("删除失败！")
      }
    },

    // 执行任务
    async runTask(row) {
      const resp = await TaskApi.runningTask(row.id)
      if (resp.success === true) {
        this.initProjectList()
        this.$message.success("开始成功！")
      } else {
        this.$message.error("执行失败！")
      }
    },
  },
}
</script>
