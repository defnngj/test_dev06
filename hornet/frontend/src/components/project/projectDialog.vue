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
        <el-input v-model="projectForm.name"></el-input>
      </el-form-item>
      <el-form-item label="描述" prop="desc">
        <el-input type="textarea" v-model="projectForm.describe"></el-input>
      </el-form-item>
      <!-- <el-form-item label="图片" prop="desc">
        <el-upload
          class="upload-demo"
          :before-upload="beforeUpload"
          :action="updateURL"
          :on-preview="handlePreview"
          :on-remove="handleRemove"
          :file-list="fileList"
          list-type="picture"
        >
          <el-button size="small" type="primary">点击上传</el-button>
          <div slot="tip" class="el-upload__tip">
            只能上传jpg/png文件，且不超过500kb
          </div>
        </el-upload>
      </el-form-item> -->
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
import ProjectApi from "../../request/project";

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
        image: "9e93a67ac46b0fb26802ef37fe237867.png",
      },
      rules: {
        name: [
          { required: true, message: "请输入项目的名称", trigger: "blur" },
        ],
      },
      fileList: [],
    };
  },
  mounted() {
    if (this.title == "create") {
      this.showTitle = "创建项目";
    } else if (this.title == "edit") {
      this.showTitle = "编辑项目";
      this.initProject();
    }
  },

  methods: {
    closeDialog() {
      console.log("closeDialog");
      this.$emit("cancel", {});
    },

    async initProject() {
      console.log("initProject");
      const resp = await ProjectApi.getProject(this.pid);
      if (resp.success === true) {
        this.projectForm = resp.item;
        this.$message.success("项目详情成功！");
      } else {
        this.$message.error("项目详情失败！");
      }
    },
    // 创建项目
    submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          console.log("标题---》", this.title);
          if (this.title == "create") {
            ProjectApi.createProject(this.projectForm).then((resp) => {
              if (resp.success === true) {
                this.closeDialog();
                this.$message.success("创建成功！");
              } else {
                this.$message.error(resp.error.message);
              }
            });
          } else if (this.title == "edit") {
            ProjectApi.updateProject(this.pid, this.projectForm).then(
              (resp) => {
                if (resp.success === true) {
                  this.closeDialog();
                  this.$message.success("编辑成功！");
                } else {
                  this.$message.error(resp.error.message);
                }
              }
            );
          }
        } else {
          return false;
        }
      });
    },

    handleRemove(file, fileList) {
      console.log(file, fileList);
    },
    handlePreview(file) {
      console.log(file);
    },

    beforeUpload(file) {
      this.importDataBtnText = "正在导入";
      this.importDataBtnIcon = "el-icon-loading";
      this.importDataDisabled = "false";
      console.log(file);
      let fd = new FormData();
      fd.append("filename", file);
      fd.append("project_id", this.project_id);
      fd.append("version_id", this.version_id);
      this.$http.post("api/projects/upload", fd).then(
        (res) => {
          console.log("res", res);
          this.importDataBtnText = "导入成功";
        },
        (res) => {
          this.importDataBtnText = "导入失败";
          console.log(res);
        }
      );
      return false;
    },
  },
};
</script>
