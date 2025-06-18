'use client'

import React, { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Textarea } from '@/components/ui/textarea'
import { Menu, Mic, Send } from 'lucide-react'

// Mock данные для транскрипта
const mockTranscript = [
  { speaker: 'Анна', message: 'Добро пожаловать на нашу встречу! Сегодня мы обсудим новый проект.' },
  { speaker: 'Михаил', message: 'Спасибо, Анна. Я готов представить наши предложения по архитектуре.' },
  { speaker: 'Елена', message: 'Отлично! Мне интересно узнать о технических деталях реализации.' },
  { speaker: 'Анна', message: 'Михаил, пожалуйста, начинай презентацию. У нас есть 30 минут.' },
  { speaker: 'Михаил', message: 'Основная идея заключается в использовании микросервисной архитектуры...' },
  { speaker: 'Елена', message: 'А как мы планируем решать вопросы с безопасностью данных?' },
]

// Mock данные для основных тезисов
const mockSummary = [
  'Обсуждение нового проекта с микросервисной архитектурой',
  'Михаил представляет техническое решение',
  'Елена поднимает вопросы безопасности данных',
  'Запланировано 30 минут на презентацию',
  'Команда готова к реализации проекта'
]

// Mock данные для Q&A
const mockQA = [
  { question: 'Какие основные технологии будут использоваться?', answer: 'Основными технологиями будут Node.js, Docker, Kubernetes и PostgreSQL для обеспечения масштабируемости и надежности системы.' },
  { question: 'Сколько времени потребуется на реализацию?', answer: 'По предварительным оценкам, полная реализация займет 3-4 месяца с учетом тестирования и внедрения.' }
]

export default function TranscriberAgent() {
  const [isRecording, setIsRecording] = useState(false)
  const [isMenuOpen, setIsMenuOpen] = useState(false)
  const [question, setQuestion] = useState('')
  const [answers, setAnswers] = useState(mockQA)

  const handleStartRecording = () => {
    setIsRecording(!isRecording)
  }

  const handleSubmitQuestion = () => {
    if (question.trim()) {
      // Здесь будет логика отправки вопроса к LLM
      const newAnswer = {
        question: question,
        answer: 'Это mock ответ на ваш вопрос. В реальной реализации здесь будет ответ от LLM на основе анализа встречи.'
      }
      setAnswers([...answers, newAnswer])
      setQuestion('')
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <h1 className="text-2xl font-bold text-gray-900">УМКА ИИ онлайн</h1>
            </div>
            <div className="relative">
              <Button
                variant="ghost"
                size="icon"
                onClick={() => setIsMenuOpen(!isMenuOpen)}
                className="p-2"
              >
                <Menu className="h-6 w-6" />
              </Button>
              
              {/* Popup Menu */}
              {isMenuOpen && (
                <div className="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg ring-1 ring-black ring-opacity-5 z-50">
                  <div className="py-1">
                    <a href="#" className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">Настройки</a>
                    <a href="#" className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">История встреч</a>
                    <a href="#" className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">Экспорт данных</a>
                    <a href="#" className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">Помощь</a>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          
          {/* Left Column - Transcript (1/3 width) */}
          <div className="lg:col-span-1">
            <Card className="h-full">
              <CardHeader>
                <CardTitle className="text-lg font-semibold">Транскрипт встречи</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4 max-h-96 overflow-y-auto">
                  {mockTranscript.map((item, index) => (
                    <div key={index} className="border-l-4 border-blue-500 pl-4">
                      <div className="font-medium text-sm text-gray-600">{item.speaker}</div>
                      <div className="text-gray-800 mt-1">{item.message}</div>
                    </div>
                  ))}
                  {isRecording && (
                    <div className="border-l-4 border-red-500 pl-4">
                      <div className="font-medium text-sm text-red-600">Запись...</div>
                      <div className="text-gray-800 mt-1 italic">Идет живая транскрипция...</div>
                    </div>
                  )}
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Right Column - Analysis & Q&A (2/3 width) */}
          <div className="lg:col-span-2 space-y-8">
            
            {/* Top Half - Summary */}
            <Card>
              <CardHeader>
                <CardTitle className="text-lg font-semibold">Основные тезисы</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {mockSummary.map((point, index) => (
                    <div key={index} className="flex items-start space-x-3">
                      <div className="flex-shrink-0 w-6 h-6 bg-blue-100 rounded-full flex items-center justify-center">
                        <span className="text-xs font-medium text-blue-600">{index + 1}</span>
                      </div>
                      <p className="text-gray-700">{point}</p>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* Bottom Half - Q&A */}
            <Card>
              <CardHeader>
                <CardTitle className="text-lg font-semibold">Вопросы и ответы</CardTitle>
              </CardHeader>
              <CardContent className="space-y-6">
                
                {/* Question Input */}
                <div className="flex space-x-2">
                  <Input
                    placeholder="Задайте вопрос о встрече..."
                    value={question}
                    onChange={(e) => setQuestion(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && handleSubmitQuestion()}
                    className="flex-1"
                  />
                  <Button onClick={handleSubmitQuestion} size="icon">
                    <Send className="h-4 w-4" />
                  </Button>
                </div>

                {/* Q&A List */}
                <div className="space-y-4 max-h-64 overflow-y-auto">
                  {answers.map((qa, index) => (
                    <div key={index} className="space-y-2">
                      <div className="bg-blue-50 rounded-lg p-3">
                        <p className="font-medium text-blue-900">В: {qa.question}</p>
                      </div>
                      <div className="bg-gray-50 rounded-lg p-3">
                        <p className="text-gray-800">О: {qa.answer}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </main>

      {/* Floating Record Button */}
      <div className="fixed bottom-8 right-8">
        <Button
          onClick={handleStartRecording}
          size="lg"
          className={`rounded-full w-16 h-16 shadow-lg transition-colors ${
            isRecording 
              ? 'bg-red-500 hover:bg-red-600 animate-pulse' 
              : 'bg-blue-500 hover:bg-blue-600'
          }`}
        >
          <Mic className="h-8 w-8" />
        </Button>
      </div>

      {/* Click outside to close menu */}
      {isMenuOpen && (
        <div 
          className="fixed inset-0 z-40" 
          onClick={() => setIsMenuOpen(false)}
        />
      )}
    </div>
  )
}
