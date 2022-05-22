import request from "@/HttpCommon.js"

class ModuleApi {
  getModuleTree(data) {
    return request.get("/api/modules/tree", data)
  }

  createModule(data) {
    return request.post("/api/modules/", data)
  }
}

export default new ModuleApi()
