<template>
  <el-dialog
    :title="showTitle"
    :visible.sync="dialogVisible"
    width="500px"
    :before-close="closeDialog"
  >
    <el-form
      :model="projectForm"
      :rules="rules"
      ref="ruleForm"
      label-width="100px"
      class="demo-ruleForm"
    >
      <el-form-item label="名称" prop="name">
        <el-input v-model="projectForm.name" cy-data="ProjectName"></el-input>
      </el-form-item>
      <el-form-item label="描述" prop="desc">
        <el-input
          type="textarea"
          v-model="projectForm.describe"
          cy-data="ProjectDescribe"
        ></el-input>
      </el-form-item>
      <el-form-item label="图片" prop="desc">
        <div id="image">
          <el-upload
            action="#"
            :before-upload="beforeUpload"
            list-type="picture-card"
            :on-preview="handlePreview"
            :on-remove="handleRemove"
            :file-list="fileList"
          >
            <i class="el-icon-plus"></i>
          </el-upload>
          <el-dialog :visible.sync="imageVisible">
            <img width="100%" :src="imageUrl" alt="" />
          </el-dialog>
        </div>
      </el-form-item>
      <el-form-item style="text-align: right">
        <el-button @click="closeDialog" cy-data="ProjectClose">取消</el-button>
        <el-button
          type="primary"
          @click="submitForm('ruleForm')"
          cy-data="ProjectOK"
          >确定</el-button
        >
      </el-form-item>
    </el-form>
  </el-dialog>
  <!-- <el-button type="danger" @click="closeDialog">关闭</el-button> -->
</template>

<script>
// import HttpCommon from "../../HttpCommon"
import ProjectApi from "../../request/project"

export default {
  name: "Dialog",
  props: ["title", "pid"],
  components: {},
  data() {
    return {
      showTitle: "",
      updateURL: "http://127.0.0.1:8000/api/projects/upload",
      dialogVisible: true,
      projectForm: {
        name: "",
        describe: "",
        image: "",
      },
      rules: {
        name: [
          { required: true, message: "请输入项目的名称", trigger: "blur" },
        ],
      },
      fileList: [],
      imageUrl: "",
      imageVisible: false,
      disabled: false,
    }
  },
  mounted() {
    if (this.title == "create") {
      this.showTitle = "创建项目"
    } else if (this.title == "edit") {
      this.showTitle = "编辑项目"
      this.initProject()
    }
  },

  methods: {
    closeDialog() {
      this.$emit("cancel", {})
    },

    // 项目详情
    async initProject() {
      const resp = await ProjectApi.getProject(this.pid)
      if (resp.success === true) {
        this.projectForm = resp.item
        this.fileList.push({
          name: resp.item.image,
          url: "static/images/" + resp.item.image,
        })
        this.$message.success("项目详情成功！")
      } else {
        this.$message.error("项目详情失败！")
      }
    },
    // 创建项目
    submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          if (this.title == "create") {
            ProjectApi.createProject(this.projectForm).then((resp) => {
              if (resp.success === true) {
                this.closeDialog()
                this.$message.success("创建成功！")
              } else {
                this.$message.error(resp.error.message)
              }
            })
          } else if (this.title == "edit") {
            ProjectApi.updateProject(this.pid, this.projectForm).then(
              (resp) => {
                if (resp.success === true) {
                  this.closeDialog()
                  this.$message.success("编辑成功！")
                } else {
                  this.$message.error(resp.error.message)
                }
              }
            )
          }
        } else {
          return false
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

    beforeUpload(file) {
      let fd = new FormData()
      fd.append("file", file)

      ProjectApi.updateImage(fd).then((resp) => {
        if (resp.data.success === true) {
          this.projectForm.image = resp.data.item.name
          const imagePath = "/static/images/" + resp.data.item.name

          this.fileList.push({
            name: file.name,
            url: imagePath,
          })
          this.$message.success("上传成功！")
        } else {
          this.$message.error(resp.error.message)
        }
      })
      return true
    },
  },
}
</script>
<style scoped>
#image {
  text-align: left;
}
</style>
