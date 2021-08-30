it('Trivial test /api', () => {
  cy.visit('/api')
})

it('Trivial test /api/cubes', () => {
  cy.visit('/api/cubes')
})

it('Check json format for /api/cubes', () => {
  cy.request('/api/cubes?format=json')
    .its('headers')
    .its('content-type')
    .should('include', 'application/json')
})
