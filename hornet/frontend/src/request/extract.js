import request from "@/HttpCommon.js"

class ExtractApi {
  getExtractList(data) {
    return request.get("/api/extracts/list", data)
  }
}

export default new ExtractApi()
