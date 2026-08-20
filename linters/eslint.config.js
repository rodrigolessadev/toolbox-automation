/**
 * Configuração de regras ESLint para UI e Acessibilidade M3
 */
export default [
  {
    files: ['**/*.{jsx,tsx}'],
    rules: {
      // Bloqueia estilos inline com cores literais hexadecimais
      'no-restricted-syntax': [
        'error',
        {
          selector: "JSXAttribute[name.name='style'] Literal[value=/^#([0-9a-fA-F]{3,8})$/]",
          message: 'Cores hardcoded em estilos inline são proibidas. Use classes do Tailwind preset M3 ou variáveis CSS var(--md-sys-color-*).'
        }
      ]
    }
  }
];
