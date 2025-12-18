# 📱 Hướng Dẫn Tích Hợp CookShare Chatbot API

**Tài liệu này hướng dẫn cách tích hợp CookBot API vào ứng dụng React Native (CookShare)**

---

## 📋 Mục Lục

1. [Tổng Quan](#tổng-quan)
2. [Base URL & Authentication](#base-url--authentication)
3. [API Endpoints](#api-endpoints)
4. [Code Examples (React Native)](#code-examples-react-native)
5. [Error Handling](#error-handling)
6. [Best Practices](#best-practices)
7. [Testing](#testing)
8. [Troubleshooting](#troubleshooting)

---

## 🎯 Tổng Quan

**CookShare Chatbot API** là một RESTful API cung cấp khả năng chat với AI tư vấn món ăn. API được deploy trên Railway và sử dụng model đã được fine-tune trên dataset nấu ăn tiếng Việt.

### Tính Năng Chính

- ✅ Gợi ý công thức từ nguyên liệu
- ✅ Hướng dẫn nấu từng bước
- ✅ Thay thế nguyên liệu
- ✅ Điều chỉnh khẩu phần
- ✅ Cảnh báo dị ứng/kiêng kỵ
- ✅ Lên lịch ăn, gợi ý theo thời tiết
- ✅ Ước tính chi phí

### Model

- **Base Model:** Qwen2-0.5B-Instruct
- **Fine-tuned:** CookShare dataset (172 samples)
- **Format:** GGUF (quantized)
- **Engine:** llama-cpp-python

---

## 🌐 Base URL & Authentication

### Base URL

```
https://llmodel-production.up.railway.app
```

**Lưu ý:** URL này có thể thay đổi nếu Railway project được rename hoặc tạo mới. Kiểm tra URL mới nhất trong Railway dashboard.

### Authentication

**Hiện tại:** Không cần authentication (public API)

**Tương lai:** Có thể thêm API key nếu cần bảo mật

---

## 🔌 API Endpoints

### 1. Health Check

Kiểm tra API có hoạt động không.

**Endpoint:** `GET /health`

**Response:**
```json
{
  "status": "healthy"
}
```

**Use Case:** Kiểm tra kết nối trước khi gửi request chat.

---

### 2. Model Info

Lấy thông tin về model đang sử dụng.

**Endpoint:** `GET /model-info`

**Response:**
```json
{
  "model_path": "models/cookshare.gguf",
  "model_loaded": true,
  "model_type": "Fine-tuned Qwen2-0.5B (cookshare.gguf)"
}
```

**Use Case:** Debug hoặc hiển thị thông tin model trong settings.

---

### 3. Simple Chat (Không có history)

Chat đơn giản, không cần lịch sử.

**Endpoint:** `POST /chat/simple?message=YOUR_MESSAGE`

**Query Parameters:**
- `message` (string, required): Câu hỏi của user

**Example:**
```
POST /chat/simple?message=Xin chào
```

**Response:**
```json
{
  "response": "Chào bạn! Tôi có thể giúp gì?",
  "success": true
}
```

**Use Case:** Câu hỏi đơn giản, không cần context từ lịch sử.

---

### 4. Chat với History (Khuyến nghị)

Chat với lịch sử hội thoại để model hiểu context.

**Endpoint:** `POST /chat`

**Request Body:**
```json
{
  "message": "Mình có trứng và cà chua, làm món gì?",
  "history": [
    {
      "role": "user",
      "content": "Xin chào"
    },
    {
      "role": "assistant",
      "content": "Chào bạn! Tôi có thể giúp gì?"
    }
  ]
}
```

**Response:**
```json
{
  "response": "Với trứng và cà chua, bạn có thể làm món trứng chiên cà chua...",
  "success": true
}
```

**Error Response:**
```json
{
  "response": "",
  "success": false,
  "error": "Error message here"
}
```

**Use Case:** Chat có context, câu hỏi phức tạp, cần lịch sử hội thoại.

---

## 💻 Code Examples (React Native)

### Setup

#### 1. Tạo API Service

Tạo file `services/ChatbotAPI.ts`:

```typescript
// services/ChatbotAPI.ts

const API_BASE_URL = 'https://llmodel-production.up.railway.app';

export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
}

export interface ChatRequest {
  message: string;
  history?: ChatMessage[];
}

export interface ChatResponse {
  response: string;
  success: boolean;
  error?: string;
}

class ChatbotAPI {
  private baseURL: string;

  constructor(baseURL: string = API_BASE_URL) {
    this.baseURL = baseURL;
  }

  /**
   * Health check - Kiểm tra API có hoạt động không
   */
  async healthCheck(): Promise<boolean> {
    try {
      const response = await fetch(`${this.baseURL}/health`);
      const data = await response.json();
      return data.status === 'healthy';
    } catch (error) {
      console.error('Health check failed:', error);
      return false;
    }
  }

  /**
   * Simple chat - Không cần history
   */
  async simpleChat(message: string): Promise<string> {
    try {
      const encodedMessage = encodeURIComponent(message);
      const response = await fetch(
        `${this.baseURL}/chat/simple?message=${encodedMessage}`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
        }
      );

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      
      if (!data.success) {
        throw new Error(data.error || 'Unknown error');
      }

      return data.response;
    } catch (error) {
      console.error('Simple chat error:', error);
      throw error;
    }
  }

  /**
   * Chat với history - Khuyến nghị dùng
   */
  async chat(message: string, history: ChatMessage[] = []): Promise<string> {
    try {
      const requestBody: ChatRequest = {
        message,
        history,
      };

      const response = await fetch(`${this.baseURL}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data: ChatResponse = await response.json();
      
      if (!data.success) {
        throw new Error(data.error || 'Unknown error');
      }

      return data.response;
    } catch (error) {
      console.error('Chat error:', error);
      throw error;
    }
  }

  /**
   * Get model info
   */
  async getModelInfo(): Promise<any> {
    try {
      const response = await fetch(`${this.baseURL}/model-info`);
      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Get model info error:', error);
      throw error;
    }
  }
}

export default new ChatbotAPI();
```

---

#### 2. Sử dụng trong Component

**Example 1: Simple Chat Component**

```typescript
// components/ChatScreen.tsx
import React, { useState } from 'react';
import { View, TextInput, Button, Text, ActivityIndicator } from 'react-native';
import ChatbotAPI, { ChatMessage } from '../services/ChatbotAPI';

const ChatScreen: React.FC = () => {
  const [message, setMessage] = useState('');
  const [response, setResponse] = useState('');
  const [loading, setLoading] = useState(false);
  const [history, setHistory] = useState<ChatMessage[]>([]);

  const handleSend = async () => {
    if (!message.trim()) return;

    setLoading(true);
    try {
      // Gửi message với history
      const botResponse = await ChatbotAPI.chat(message, history);
      
      // Cập nhật history
      const newHistory: ChatMessage[] = [
        ...history,
        { role: 'user', content: message },
        { role: 'assistant', content: botResponse },
      ];
      setHistory(newHistory);
      
      // Hiển thị response
      setResponse(botResponse);
      
      // Clear input
      setMessage('');
    } catch (error) {
      console.error('Chat error:', error);
      setResponse('Xin lỗi, có lỗi xảy ra. Vui lòng thử lại.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <View style={{ padding: 20 }}>
      <TextInput
        value={message}
        onChangeText={setMessage}
        placeholder="Nhập câu hỏi..."
        multiline
        style={{
          borderWidth: 1,
          borderColor: '#ccc',
          borderRadius: 8,
          padding: 10,
          marginBottom: 10,
          minHeight: 50,
        }}
      />
      
      <Button title="Gửi" onPress={handleSend} disabled={loading} />
      
      {loading && <ActivityIndicator style={{ marginTop: 20 }} />}
      
      {response && (
        <View style={{ marginTop: 20, padding: 10, backgroundColor: '#f0f0f0', borderRadius: 8 }}>
          <Text>{response}</Text>
        </View>
      )}
    </View>
  );
};

export default ChatScreen;
```

---

**Example 2: Chat với History (Full Implementation)**

```typescript
// components/ChatBot.tsx
import React, { useState, useRef, useEffect } from 'react';
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  FlatList,
  ActivityIndicator,
  StyleSheet,
} from 'react-native';
import ChatbotAPI, { ChatMessage } from '../services/ChatbotAPI';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

const ChatBot: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputText, setInputText] = useState('');
  const [loading, setLoading] = useState(false);
  const [apiHealthy, setApiHealthy] = useState<boolean | null>(null);
  const flatListRef = useRef<FlatList>(null);

  // Check API health on mount
  useEffect(() => {
    checkAPIHealth();
  }, []);

  const checkAPIHealth = async () => {
    const healthy = await ChatbotAPI.healthCheck();
    setApiHealthy(healthy);
  };

  const sendMessage = async () => {
    if (!inputText.trim() || loading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: inputText.trim(),
      timestamp: new Date(),
    };

    // Add user message to UI immediately
    setMessages((prev) => [...prev, userMessage]);
    setInputText('');
    setLoading(true);

    try {
      // Convert messages to ChatMessage format for API
      const history: ChatMessage[] = messages.map((msg) => ({
        role: msg.role,
        content: msg.content,
      }));

      // Call API
      const response = await ChatbotAPI.chat(userMessage.content, history);

      // Add bot response
      const botMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: response,
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, botMessage]);

      // Scroll to bottom
      setTimeout(() => {
        flatListRef.current?.scrollToEnd({ animated: true });
      }, 100);
    } catch (error) {
      console.error('Send message error:', error);
      
      // Add error message
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: 'Xin lỗi, có lỗi xảy ra. Vui lòng thử lại sau.',
        timestamp: new Date(),
      };
      
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const renderMessage = ({ item }: { item: Message }) => {
    const isUser = item.role === 'user';
    
    return (
      <View
        style={[
          styles.messageContainer,
          isUser ? styles.userMessage : styles.botMessage,
        ]}
      >
        <Text style={isUser ? styles.userText : styles.botText}>
          {item.content}
        </Text>
      </View>
    );
  };

  return (
    <View style={styles.container}>
      {/* API Status */}
      {apiHealthy !== null && (
        <View style={styles.statusBar}>
          <Text style={styles.statusText}>
            {apiHealthy ? '🟢 API Online' : '🔴 API Offline'}
          </Text>
        </View>
      )}

      {/* Messages List */}
      <FlatList
        ref={flatListRef}
        data={messages}
        renderItem={renderMessage}
        keyExtractor={(item) => item.id}
        contentContainerStyle={styles.messagesList}
        onContentSizeChange={() => {
          flatListRef.current?.scrollToEnd({ animated: true });
        }}
      />

      {/* Input Area */}
      <View style={styles.inputContainer}>
        <TextInput
          value={inputText}
          onChangeText={setInputText}
          placeholder="Nhập câu hỏi..."
          multiline
          style={styles.input}
          editable={!loading}
        />
        <TouchableOpacity
          onPress={sendMessage}
          disabled={loading || !inputText.trim()}
          style={[
            styles.sendButton,
            (loading || !inputText.trim()) && styles.sendButtonDisabled,
          ]}
        >
          {loading ? (
            <ActivityIndicator color="#fff" />
          ) : (
            <Text style={styles.sendButtonText}>Gửi</Text>
          )}
        </TouchableOpacity>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
  },
  statusBar: {
    padding: 8,
    backgroundColor: '#f0f0f0',
    alignItems: 'center',
  },
  statusText: {
    fontSize: 12,
    color: '#666',
  },
  messagesList: {
    padding: 16,
  },
  messageContainer: {
    maxWidth: '80%',
    padding: 12,
    borderRadius: 12,
    marginBottom: 8,
  },
  userMessage: {
    alignSelf: 'flex-end',
    backgroundColor: '#007AFF',
  },
  botMessage: {
    alignSelf: 'flex-start',
    backgroundColor: '#E5E5EA',
  },
  userText: {
    color: '#fff',
    fontSize: 16,
  },
  botText: {
    color: '#000',
    fontSize: 16,
  },
  inputContainer: {
    flexDirection: 'row',
    padding: 16,
    borderTopWidth: 1,
    borderTopColor: '#E5E5EA',
    alignItems: 'flex-end',
  },
  input: {
    flex: 1,
    borderWidth: 1,
    borderColor: '#E5E5EA',
    borderRadius: 20,
    paddingHorizontal: 16,
    paddingVertical: 10,
    maxHeight: 100,
    marginRight: 8,
  },
  sendButton: {
    backgroundColor: '#007AFF',
    paddingHorizontal: 20,
    paddingVertical: 10,
    borderRadius: 20,
    justifyContent: 'center',
    alignItems: 'center',
  },
  sendButtonDisabled: {
    backgroundColor: '#ccc',
  },
  sendButtonText: {
    color: '#fff',
    fontWeight: 'bold',
  },
});

export default ChatBot;
```

---

## ⚠️ Error Handling

### Common Errors

#### 1. Network Error

```typescript
try {
  const response = await ChatbotAPI.chat(message);
} catch (error) {
  if (error.message.includes('Network request failed')) {
    // Không có internet
    showError('Không có kết nối internet. Vui lòng kiểm tra lại.');
  } else {
    // Lỗi khác
    showError('Có lỗi xảy ra. Vui lòng thử lại.');
  }
}
```

#### 2. API Error (500, 400, etc.)

```typescript
try {
  const response = await ChatbotAPI.chat(message);
} catch (error) {
  if (error.message.includes('HTTP error! status: 500')) {
    // Server error
    showError('Server đang gặp sự cố. Vui lòng thử lại sau.');
  } else if (error.message.includes('HTTP error! status: 400')) {
    // Bad request
    showError('Câu hỏi không hợp lệ. Vui lòng thử lại.');
  }
}
```

#### 3. Timeout

```typescript
// Thêm timeout cho fetch
const controller = new AbortController();
const timeoutId = setTimeout(() => controller.abort(), 30000); // 30 seconds

try {
  const response = await fetch(url, {
    ...options,
    signal: controller.signal,
  });
  clearTimeout(timeoutId);
} catch (error) {
  if (error.name === 'AbortError') {
    showError('Request timeout. Vui lòng thử lại.');
  }
}
```

### Error Handling Helper

```typescript
// utils/errorHandler.ts
export const handleChatError = (error: any): string => {
  if (error.message?.includes('Network request failed')) {
    return 'Không có kết nối internet. Vui lòng kiểm tra lại.';
  }
  
  if (error.message?.includes('HTTP error! status: 500')) {
    return 'Server đang gặp sự cố. Vui lòng thử lại sau.';
  }
  
  if (error.message?.includes('HTTP error! status: 400')) {
    return 'Câu hỏi không hợp lệ. Vui lòng thử lại.';
  }
  
  if (error.message?.includes('timeout')) {
    return 'Request timeout. Vui lòng thử lại.';
  }
  
  return 'Có lỗi xảy ra. Vui lòng thử lại.';
};
```

---

## 🎯 Best Practices

### 1. Caching History

Lưu lịch sử chat vào AsyncStorage để giữ context khi app restart:

```typescript
import AsyncStorage from '@react-native-async-storage/async-storage';

const HISTORY_KEY = '@chatbot_history';

// Save history
const saveHistory = async (history: ChatMessage[]) => {
  try {
    await AsyncStorage.setItem(HISTORY_KEY, JSON.stringify(history));
  } catch (error) {
    console.error('Save history error:', error);
  }
};

// Load history
const loadHistory = async (): Promise<ChatMessage[]> => {
  try {
    const data = await AsyncStorage.getItem(HISTORY_KEY);
    return data ? JSON.parse(data) : [];
  } catch (error) {
    console.error('Load history error:', error);
    return [];
  }
};
```

### 2. Debounce Input

Tránh gửi quá nhiều request:

```typescript
import { debounce } from 'lodash';

const debouncedSend = debounce(async (message: string) => {
  await ChatbotAPI.chat(message);
}, 500);
```

### 3. Loading States

Luôn hiển thị loading state khi đang gửi request:

```typescript
const [loading, setLoading] = useState(false);

const handleSend = async () => {
  setLoading(true);
  try {
    await ChatbotAPI.chat(message);
  } finally {
    setLoading(false);
  }
};
```

### 4. Retry Logic

Thêm retry khi request fail:

```typescript
const retryChat = async (
  message: string,
  history: ChatMessage[],
  maxRetries = 3
): Promise<string> => {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await ChatbotAPI.chat(message, history);
    } catch (error) {
      if (i === maxRetries - 1) throw error;
      await new Promise((resolve) => setTimeout(resolve, 1000 * (i + 1))); // Exponential backoff
    }
  }
  throw new Error('Max retries exceeded');
};
```

### 5. Response Timeout

Set timeout cho mỗi request:

```typescript
const chatWithTimeout = async (
  message: string,
  history: ChatMessage[],
  timeout = 30000
): Promise<string> => {
  return Promise.race([
    ChatbotAPI.chat(message, history),
    new Promise<string>((_, reject) =>
      setTimeout(() => reject(new Error('Request timeout')), timeout)
    ),
  ]);
};
```

---

## 🧪 Testing

### 1. Test với Postman

Xem file `POSTMAN_TEST.md` để test API với Postman.

### 2. Test trong React Native

```typescript
// __tests__/ChatbotAPI.test.ts
import ChatbotAPI from '../services/ChatbotAPI';

describe('ChatbotAPI', () => {
  test('health check should return true', async () => {
    const result = await ChatbotAPI.healthCheck();
    expect(result).toBe(true);
  });

  test('simple chat should return response', async () => {
    const response = await ChatbotAPI.simpleChat('Xin chào');
    expect(response).toBeTruthy();
    expect(typeof response).toBe('string');
  });

  test('chat with history should return response', async () => {
    const history = [
      { role: 'user' as const, content: 'Xin chào' },
      { role: 'assistant' as const, content: 'Chào bạn!' },
    ];
    const response = await ChatbotAPI.chat('Mình có trứng', history);
    expect(response).toBeTruthy();
  });
});
```

### 3. Test Cases

**Test Case 1: Gợi ý công thức**
```
Input: "Mình có trứng và cà chua, làm món gì?"
Expected: Model gợi ý các món như trứng chiên cà chua, canh trứng cà chua
```

**Test Case 2: Hướng dẫn nấu**
```
Input: "Cách làm phở bò?"
Expected: Model trả lời với các bước chi tiết, nguyên liệu, thời gian
```

**Test Case 3: Chat với history**
```
Input: "Làm thế nào để nấu?" (sau khi đã hỏi về phở bò)
Expected: Model hiểu context và trả lời về cách nấu phở bò
```

---

## 🔧 Troubleshooting

### 1. API không phản hồi

**Nguyên nhân:**
- Railway service đang sleep (free tier)
- Network issue
- API URL sai

**Giải pháp:**
- Kiểm tra Railway dashboard xem service có đang chạy không
- Test API với Postman trước
- Kiểm tra URL trong code

### 2. Response quá chậm

**Nguyên nhân:**
- Model đang xử lý câu hỏi phức tạp
- Railway CPU limit
- Network latency

**Giải pháp:**
- Thêm timeout và loading state
- Hiển thị "Đang suy nghĩ..." cho user
- Cân nhắc upgrade Railway plan

### 3. Response không đúng

**Nguyên nhân:**
- Model chưa được train đủ
- Câu hỏi quá phức tạp
- History không đúng format

**Giải pháp:**
- Kiểm tra format history (phải là array of {role, content})
- Thử câu hỏi đơn giản hơn
- Kiểm tra model info endpoint

### 4. CORS Error

**Nguyên nhân:**
- API chưa config CORS đúng

**Giải pháp:**
- API đã config CORS cho phép tất cả origins
- Nếu vẫn lỗi, kiểm tra lại API code

---

## 📞 Support

Nếu gặp vấn đề, vui lòng:

1. Kiểm tra Railway logs
2. Test API với Postman
3. Kiểm tra Network tab trong React Native debugger
4. Xem file `API_ENDPOINTS.md` và `POSTMAN_TEST.md` để biết thêm chi tiết

---

## 📝 Changelog

### v1.0.0 (2024-12-18)
- ✅ Initial release
- ✅ Simple chat endpoint
- ✅ Chat with history endpoint
- ✅ Health check endpoint
- ✅ Model info endpoint

---

## 🔗 Links

- **API Base URL:** `https://llmodel-production.up.railway.app`
- **API Docs:** Xem `API_ENDPOINTS.md`
- **Postman Tests:** Xem `POSTMAN_TEST.md`
- **Railway Dashboard:** [railway.app](https://railway.app)

---

**Happy Coding! 🚀**

