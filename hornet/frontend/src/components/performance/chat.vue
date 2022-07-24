<template>
  <div class="home">
    <div>
      <div style="margin-bottom: 10px">
        <el-input
          type="textarea"
          :rows="10"
          placeholder="聊天窗口"
          v-model="textarea"
        >
        </el-input>
      </div>
      <div style="margin-bottom: 10px">
        <el-input v-model="input" placeholder="请输入消息"></el-input>
      </div>
      <div style="margin-bottom: 10px; text-align: left">
        <el-button type="primary" @click="onSubmit">发送</el-button>
      </div>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src

export default {
  name: "Porject",
  components: {
    //组件
  },
  data() {
    return {
      socket: "",
      textarea: "",
      input: "",
    }
  },
  mounted() {
    this.initConn()
  },
  methods: {
    // 初始化项目列表
    initConn() {
      const wss_protocol =
        window.location.protocol == "https:" ? "wss://" : "ws://"
      // this.socket = new WebSocket(
      //   wss_protocol + window.location.host + "/ws/performance/chat/"
      // )
      this.socket = new WebSocket(
        wss_protocol + "127.0.0.1:8000/ws/performance/chat/room/"
      )
      this.socket.onopen = this.onOpen
      this.socket.onmessage = this.onMessage
      this.socket.onclose = this.onClose
    },

    onOpen() {
      this.textarea +=
        this.textarea + "[公告]欢迎来到vue.js讨论群。请文明发言!\n"
      // let mes = {}
      // mes.type = "test"
      // this.socket.send(JSON.stringify(mes))
    },

    onMessage(e) {
      console.log("on-msg", e)
      const data = JSON.parse(e.data)
      console.log("data-->", data)
      this.textarea += "\n" + data.message
    },

    onClose(e) {
      console.error("e", e)
    },

    onSubmit() {
      this.textarea += "Me：" + this.input
      this.socket.send(
        JSON.stringify({
          message: this.input,
        })
      )
    },
  },
}
</script>
