// https://docs.cypress.io/api/introduction/api.html

describe("My First Test", () => {
  it("home", () => {
    cy.visit("/");
    cy.contains("h1", "This is HelloWorld page.");
  });
  it("about", () => {
    cy.visit("/about");
    cy.contains("h1", "This is an about page");
  });
});
