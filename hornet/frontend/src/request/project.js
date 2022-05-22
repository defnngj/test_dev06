import request from "@/HttpCommon.js"
import axios from "axios"

class ProjectApi {
  getProjects(data) {
    return request.get("/api/projects/list", data)
  }

  getProject(id) {
    return request.get("/api/projects/" + id + "/")
  }

  updateProject(id, data) {
    return request.put("/api/projects/" + id + "/", data)
  }

  deleteProject(id) {
    return request.delete("/api/projects/" + id + "/")
  }

  createProject(data) {
    return request.post("/api/projects/", data)
  }

  updateImage(data) {
    return axios({
      method: "post",
      url: "/api/projects/upload",
      timeout: 20000,
      data: data,
    })
  }
}

export default new ProjectApi()
