export const formatInches = (inches: number) => {
  if (inches < 9 && inches > 8.5) return 8.5;
  return Math.floor(inches);
};

const mediumChoices = [
  { key: 'oil_panel', value: 'Oil on Panel' },
  { key: 'acrylic_panel', value: 'Acrylic on Panel' },
  { key: 'oil_mdf', value: 'Oil on MDF' },
  { key: 'oil_paper', value: 'Oil on Oil Paper' },
  { key: 'unknown', value: 'Unknown' },
];

export const getMedium = (medium: string) => mediumChoices.find((choice) => choice.key === medium)?.value || medium;
