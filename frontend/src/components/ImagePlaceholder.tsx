import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { colors } from '../theme/colors';

interface ImagePlaceholderProps {
  type?: 'sign' | 'road' | 'vehicle' | 'generic';
  size?: 'small' | 'medium' | 'large';
}

const typeConfig = {
  sign: {
    icon: '🚦',
    label: 'Imagem da placa',
    bgColor: '#FEF3C7',
    borderColor: '#F59E0B',
  },
  road: {
    icon: '🛣️',
    label: 'Imagem da via',
    bgColor: '#DBEAFE',
    borderColor: '#3B82F6',
  },
  vehicle: {
    icon: '🚗',
    label: 'Imagem do veículo',
    bgColor: '#D1FAE5',
    borderColor: '#10B981',
  },
  generic: {
    icon: '🖼️',
    label: 'Imagem ilustrativa',
    bgColor: '#F3E8FF',
    borderColor: '#8B5CF6',
  },
};

const sizeConfig = {
  small: { height: 80, iconSize: 28, fontSize: 10 },
  medium: { height: 120, iconSize: 36, fontSize: 12 },
  large: { height: 160, iconSize: 48, fontSize: 14 },
};

/**
 * Detects the type of image placeholder based on question text keywords
 */
export function detectImageType(questionText: string): 'sign' | 'road' | 'vehicle' | 'generic' | null {
  const text = questionText.toLowerCase();
  
  const signKeywords = [
    'placa', 'sinal', 'sinalização', 'semáforo', 'faixa de pedestres',
    'faixa contínua', 'faixa tracejada', 'faixa dupla', 'seta', 'indicação',
    'regulamentação', 'advertência', 'proibido', 'permitido', 'lombada',
    'ciclovia', 'ciclofaixa', 'rotatória', 'pare', 'velocidade máxima',
  ];
  
  const roadKeywords = [
    'via', 'rodovia', 'estrada', 'pista', 'cruzamento', 'interseção',
    'túnel', 'ponte', 'viaduto', 'acostamento', 'curva',
  ];
  
  const vehicleKeywords = [
    'retrovisor', 'painel', 'farol', 'lanterna', 'pneu', 'roda',
    'para-brisa', 'limpador', 'extintor', 'triângulo', 'estepe',
    'cadeirinha', 'bebê conforto', 'airbag', 'cinto',
  ];
  
  // Only show placeholder for questions that specifically mention visual references
  const visualReferenceKeywords = [
    'figura', 'imagem', 'ilustração', 'observe', 'veja',
    'representada', 'representado', 'mostrada', 'mostrado',
    'indica a', 'indica o', 'significa a placa', 'significa o sinal',
    'placa de', 'sinal de',
  ];
  
  // Check if question references a visual element
  const hasVisualRef = visualReferenceKeywords.some(kw => text.includes(kw));
  
  // For Module 1 (signs), many questions naturally reference signs
  const isSignQuestion = signKeywords.some(kw => text.includes(kw));
  const isRoadQuestion = roadKeywords.some(kw => text.includes(kw));
  const isVehicleQuestion = vehicleKeywords.some(kw => text.includes(kw));
  
  if (hasVisualRef) {
    if (isSignQuestion) return 'sign';
    if (isRoadQuestion) return 'road';
    if (isVehicleQuestion) return 'vehicle';
    return 'generic';
  }
  
  return null;
}

export const ImagePlaceholder: React.FC<ImagePlaceholderProps> = ({
  type = 'generic',
  size = 'medium',
}) => {
  const config = typeConfig[type];
  const dimensions = sizeConfig[size];

  return (
    <View
      style={[
        styles.container,
        {
          height: dimensions.height,
          backgroundColor: config.bgColor,
          borderColor: config.borderColor,
        },
      ]}
    >
      <Text style={[styles.icon, { fontSize: dimensions.iconSize }]}>{config.icon}</Text>
      <Text style={[styles.label, { fontSize: dimensions.fontSize, color: config.borderColor }]}>
        {config.label}
      </Text>
      <Text style={[styles.sublabel, { fontSize: dimensions.fontSize - 2, color: config.borderColor + '99' }]}>
        Será adicionada em breve
      </Text>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    borderRadius: 12,
    borderWidth: 2,
    borderStyle: 'dashed',
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 12,
  },
  icon: {
    marginBottom: 6,
  },
  label: {
    fontWeight: '600',
    marginBottom: 2,
  },
  sublabel: {
    fontWeight: '400',
  },
});
