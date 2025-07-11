import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import { StatusBar } from 'expo-status-bar';
import { SafeAreaProvider } from 'react-native-safe-area-context';

import HomeScreen from './src/screens/HomeScreen';
import PuzzleScreen from './src/screens/PuzzleScreen';
import HeadsUpScreen from './src/screens/HeadsUpScreen';
import { PuzzleProvider } from './src/context/PuzzleContext';

const Stack = createStackNavigator();

export default function App() {
  return (
    <SafeAreaProvider>
      <PuzzleProvider>
        <NavigationContainer>
          <Stack.Navigator
            initialRouteName="Home"
            screenOptions={{
              headerStyle: {
                backgroundColor: '#1a1a1a',
              },
              headerTintColor: '#fff',
              headerTitleStyle: {
                fontWeight: 'bold',
              },
            }}
          >
            <Stack.Screen 
              name="Home" 
              component={HomeScreen} 
              options={{ title: 'Poker Trainer' }}
            />
            <Stack.Screen 
              name="Puzzle" 
              component={PuzzleScreen} 
              options={{ title: 'Puzzle' }}
            />
            <Stack.Screen 
              name="HeadsUp" 
              component={HeadsUpScreen} 
              options={{ title: 'Heads-Up Poker' }}
            />
          </Stack.Navigator>
          <StatusBar style="light" />
        </NavigationContainer>
      </PuzzleProvider>
    </SafeAreaProvider>
  );
} 