#!/bin/bash

echo "🎰 Setting up Poker Trainer App..."

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js first."
    exit 1
fi

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed. Please install npm first."
    exit 1
fi

echo "📦 Installing dependencies..."
npm install

echo "✅ Dependencies installed successfully!"
echo ""
echo "🚀 To start the app:"
echo "   npm start"
echo ""
echo "🌐 For web development:"
echo "   Press 'w' when the Expo server starts"
echo ""
echo "📱 For mobile development:"
echo "   - Install Expo Go app on your phone"
echo "   - Scan the QR code when the server starts"
echo ""
echo "🔧 Make sure your Python backend is running:"
echo "   cd poker/server"
echo "   uvicorn main:app --reload"
echo ""
echo "🎉 Setup complete! Happy poker training!" 