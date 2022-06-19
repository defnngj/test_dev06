import request from "@/HttpCommon.js"

class TaskApi {
  createTask(data) {
    return request.post("/api/tasks/", data)
  }

  getTaskList(data) {
    return request.get("/api/tasks/list", data)
  }

  getTaskDetail(tid) {
    return request.get("/api/tasks/" + tid + "/")
  }

  updateTask(tid, data) {
    return request.put("/api/tasks/" + tid + "/", data)
  }

  deleteTask(tid) {
    return request.delete("/api/tasks/" + tid + "/")
  }

  runningTask(tid) {
    return request.post("/api/tasks/" + tid + "/running")
  }
}

export default new TaskApi()
