// https://docs.cypress.io/api/introduction/api.html

describe("test home Login", () => {
  it("home", () => {
    cy.visit("/")
    cy.contains("h2", "接口测试平台")
  })
  it("login", () => {
    cy.visit("/login")
    cy.get("[cy-data=LoginUsername]", { timeout: 3000 }).clear()
    cy.get("[cy-data=LoginUsername]", { timeout: 3000 }).type("tom")
    cy.get("[cy-data=LoginPassword]", { timeout: 3000 }).clear()
    cy.get("[cy-data=LoginPassword]", { timeout: 3000 }).type("tom123456")
    cy.get("[cy-data=loginButton]", { timeout: 3000 }).click()
    cy.contains("[cy-data=loginSuccess]", "欢迎~ tom")
  })
})
