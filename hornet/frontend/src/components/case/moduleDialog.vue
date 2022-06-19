<template>
  <el-dialog
    :title="showTitle"
    :visible.sync="dialogVisible"
    width="500px"
    :before-close="closeDialog"
  >
    <el-form
      :model="moduleForm"
      :rules="rules"
      ref="ruleForm"
      label-width="100px"
      class="demo-ruleForm"
    >
      <el-form-item label="项目" prop="name">
        <el-input v-model="projectLabel" disabled></el-input>
      </el-form-item>
      <el-form-item label="父节点" v-if="parentObj.label !== ''">
        <el-input v-model="parentObj.label" disabled></el-input>
      </el-form-item>
      <el-form-item label="名称" prop="name">
        <el-input v-model="moduleForm.name"></el-input>
      </el-form-item>
      <el-form-item style="text-align: right">
        <el-button @click="closeDialog">取消</el-button>
        <el-button type="primary" @click="submitForm('ruleForm')"
          >确定</el-button
        >
      </el-form-item>
    </el-form>
  </el-dialog>
  <!-- <el-button type="danger" @click="closeDialog">关闭</el-button> -->
</template>

<script>
import ModuleApi from "../../request/module"

export default {
  name: "Dialog",
  props: ["projectId", "projectLabel", "rootId", "parentObj"],
  components: {},
  data() {
    return {
      showTitle: "",
      updateURL: "http://127.0.0.1:8000/api/projects/upload",
      dialogVisible: true,
      moduleForm: {
        name: "",
        project_id: 0,
        parent_id: 0,
      },
      rules: {
        name: [
          { required: true, message: "请输入模块的名称", trigger: "blur" },
        ],
      },
      fileList: [],
      imageUrl: "",
      imageVisible: false,
      disabled: false,
    }
  },
  mounted() {
    this.moduleForm.project_id = this.projectId

    if (this.rootId == true) {
      this.showTitle = "创建根节点"
    } else {
      this.showTitle = "创建子节点"
      this.moduleForm.parent_id = this.parentObj.id
    }
  },

  methods: {
    closeDialog() {
      this.$emit("cancel", {})
    },

    // 创建模块
    submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          ModuleApi.createModule(this.moduleForm).then((resp) => {
            if (resp.success === true) {
              this.closeDialog()
              this.$message.success("创建成功！")
            } else {
              this.$message.error(resp.error.msg)
            }
          })
        }
      })
    },

    // 删除图片
    handleRemove(file) {
      console.log("删除", file)
    },

    // 预览图片
    handlePreview(file, fileList) {
      console.log(fileList)
      this.imageUrl = file.url
      this.imageVisible = true
    },
  },
}
</script>
<style scoped>
#image {
  text-align: left;
}
</style>
