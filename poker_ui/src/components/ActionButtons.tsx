import React from 'react';
import { View, TouchableOpacity, Text, StyleSheet } from 'react-native';

interface ActionButtonsProps {
  onAction: (action: string) => void;
  disabled?: boolean;
}

const ActionButtons: React.FC<ActionButtonsProps> = ({ onAction, disabled = false }) => {
  const actions = [
    { label: 'Fold', color: '#ff4444', action: 'fold' },
    { label: 'Check/Call', color: '#4CAF50', action: 'call' },
    { label: 'Raise', color: '#ff9800', action: 'raise' },
  ];

  return (
    <View style={styles.container}>
      {actions.map(({ label, color, action }) => (
        <TouchableOpacity
          key={action}
          style={[styles.button, { backgroundColor: color }, disabled && styles.disabled]}
          onPress={() => onAction(action)}
          disabled={disabled}
        >
          <Text style={styles.buttonText}>{label}</Text>
        </TouchableOpacity>
      ))}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    padding: 20,
    backgroundColor: '#2a2a2a',
  },
  button: {
    paddingHorizontal: 20,
    paddingVertical: 12,
    borderRadius: 8,
    minWidth: 80,
    alignItems: 'center',
  },
  buttonText: {
    color: '#ffffff',
    fontSize: 16,
    fontWeight: 'bold',
  },
  disabled: {
    opacity: 0.5,
  },
});

export default ActionButtons; 