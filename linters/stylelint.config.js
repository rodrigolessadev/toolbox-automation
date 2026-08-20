/**
 * Configuração oficial de Stylelint para Material Design 3 (M3)
 * Proíbe cores literais (#HEX, rgb, hsl) fora de arquivos de definição mestre de tema.
 */
export default {
  extends: ['stylelint-config-standard'],
  rules: {
    // Proíbe cores hexadecimais literais
    'color-no-hex': [
      true,
      {
        message: 'Cores hexadecimais hardcoded são proibidas. Use tokens semânticos var(--md-sys-color-*) do Material Design 3.'
      }
    ],
    // Bloqueia valores diretos de cores que não usem variáveis
    'declaration-property-value-disallowed-list': [
      {
        '/^color/': ['/^rgb/', '/^hsl/'],
        '/^background/': ['/^rgb/', '/^hsl/'],
        '/^border/': ['/^rgb/', '/^hsl/']
      },
      {
        message: 'Funções de cor direta (rgb/hsl) são proibidas. Utilize variáveis semânticas var(--md-sys-color-*).'
      }
    ]
  },
  ignoreFiles: [
    '**/theme.css',
    '**/tokens.json',
    '**/dist/**',
    '**/node_modules/**'
  ]
};
