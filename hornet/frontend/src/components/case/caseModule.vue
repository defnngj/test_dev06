<template>
  <div class="case">
    <div style="text-align: left">
      <el-form :inline="true">
        <el-form-item label="项目">
          <el-select
            v-model="projectValue"
            size="medium"
            placeholder="请选择项目"
            @change="changeProject"
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
          <el-button type="primary" size="medium" @click="createCase()"
            >创建用例</el-button
          >
        </el-form-item>
      </el-form>
    </div>
    <div style="margin-top: 10px">
      <el-card style="width: 28%; float: left">
        <el-button
          type="text"
          icon="el-icon-circle-plus-outline"
          @click="createRootModule"
          >根节点</el-button
        >
        <el-tree
          :data="moduleData"
          node-key="id"
          default-expand-all
          :expand-on-click-node="false"
          @node-click="nodeClick"
        >
          <span class="custom-tree-node" slot-scope="{ node, data }">
            <span style="float: left">{{ node.label }}</span>
            <span style="float: right">
              <el-button type="text" size="mini" @click="() => append(data)">
                <i class="el-icon-circle-plus-outline"></i>
              </el-button>
              <el-button
                type="text"
                size="mini"
                @click="() => remove(node, data)"
              >
                <i class="el-icon-delete"></i>
              </el-button>
            </span>
          </span>
        </el-tree>
      </el-card>
      <div style="width: 70%; float: right">
        <el-table
          :data="casesData"
          border
          style="width: 100%"
          @row-click="caseRowClick"
        >
          <el-table-column prop="id" label="ID" width="50"> </el-table-column>
          <el-table-column prop="name" label="名称" width="180">
          </el-table-column>
          <el-table-column prop="method" label="方法" width="80">
          </el-table-column>
          <el-table-column prop="url" label="URL" width="180">
          </el-table-column>
          <el-table-column prop="module.name" label="模块" width="100">
          </el-table-column>
          <el-table-column prop="create_time" label="创建时间">
          </el-table-column>
        </el-table>
      </div>

      <el-drawer
        :title="caseTitle"
        :visible.sync="drawer"
        direction="rtl"
        size="50%"
      >
        <CaseDialog
          v-if="drawer"
          :mid="currentModule"
          :cid="currentCase"
        ></CaseDialog>
      </el-drawer>
    </div>

    <!-- 创建模块 -->
    <moduleDialog
      v-if="dialogFlag"
      :projectId="projectValue"
      :projectLabel="projectLabel"
      :rootId="rootFlag"
      :parentObj="parentObj"
      @cancel="closeDialog"
    >
    </moduleDialog>
  </div>
</template>

<script>
import ProjectApi from "../../request/project"
import ModuleApi from "../../request/module"
import moduleDialog from "./moduleDialog.vue"
import CaseDialog from "./CaseDialog.vue"

export default {
  name: "HelloWorld",
  components: {
    moduleDialog,
    CaseDialog,
  },
  data() {
    return {
      projectValue: 1,
      projectLabel: "",
      rootFlag: true,
      projectOption: [],
      moduleData: [],
      dialogFlag: false,
      parentObj: {},
      casesData: [],
      drawer: false,
      caseTitle: "",
      currentModule: 0, // 当前选中的模块
      currentCase: 0, // 当前选中的用例
    }
  },
  mounted() {
    this.initProjectList()
    this.initModuleList(this.projectValue)
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

    // 修改选中项目
    changeProject(value) {
      this.projectValue = value
      this.projectLabel = this.projectOption.find(
        (item) => item.value === value
      ).label
      this.initModuleList(value)
    },

    // 查询模块列表
    async initModuleList(pid) {
      const req = { project_id: pid }
      const resp = await ModuleApi.getModuleTree(req)
      if (resp.success === true) {
        this.moduleData = resp.items
        // this.$message.success("查询成功！")
      } else {
        this.$message.error("查询失败！")
      }
    },

    // 添加子节点
    append(data) {
      this.dialogFlag = true
      this.rootFlag = false
      this.parentObj = data
    },

    // 移除子节点
    remove(node, data) {
      ModuleApi.deleteModule(data.id).then((resp) => {
        if (resp.success === true) {
          this.$message.success("删除成功！")
          this.initModuleList(this.projectValue)
        } else {
          this.$message.error(resp.error.msg)
        }
      })
    },

    // 创建根节点
    createRootModule() {
      this.dialogFlag = true
      this.rootFlag = true
    },

    // 创建模块关闭
    closeDialog() {
      this.dialogFlag = false
      this.parentObj = {}
      this.initModuleList(this.projectValue)
    },

    // 点击模块
    nodeClick(data) {
      this.currentModule = data.id
      this.getCaseList(data.id)
    },

    async getCaseList(mid) {
      const resp = await ModuleApi.getModuleCase(mid)
      if (resp.success === true) {
        this.casesData = resp.items
        this.$message.success("查询成功！")
      } else {
        this.$message.error("查询失败！")
      }
    },

    createCase() {
      this.drawer = true
      this.caseTitle = "创建用例"
    },

    caseRowClick(row) {
      this.currentCase = row.id
      this.drawer = true
      this.caseTitle = "查看用例"
    },
  },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.custom-tree-node {
  width: 100%;
}
</style>
