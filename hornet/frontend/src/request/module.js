import request from "@/HttpCommon.js"

class ModuleApi {
  getModuleTree(data) {
    return request.get("/api/modules/tree", data)
  }

  createModule(data) {
    return request.post("/api/modules/", data)
  }

  deleteModule(mid) {
    return request.delete("/api/modules/" + mid + "/")
  }

  getModuleCase(mid) {
    return request.get("/api/modules/" + mid + "/cases")
  }
}

export default new ModuleApi()
