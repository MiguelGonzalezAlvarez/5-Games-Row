import { useEffect, useState, useCallback, useRef } from 'react';

type Channel = 'match_updates' | 'challenge_updates' | 'standings_updates' | 'general';

interface WebSocketMessage {
  type: string;
  data?: any;
}

interface UseWebSocketOptions {
  channel: Channel;
  autoReconnect?: boolean;
  reconnectInterval?: number;
  onMessage?: (message: WebSocketMessage) => void;
  onConnect?: () => void;
  onDisconnect?: () => void;
  onError?: (error: Event) => void;
  token?: string;
}

export function useWebSocket({
  channel,
  autoReconnect = true,
  reconnectInterval = 3000,
  onMessage,
  onConnect,
  onDisconnect,
  onError,
  token,
}: UseWebSocketOptions) {
  const [isConnected, setIsConnected] = useState(false);
  const [lastMessage, setLastMessage] = useState<WebSocketMessage | null>(null);
  const wsRef = useRef<WebSocket | null>(null);
  const reconnectTimeoutRef = useRef<NodeJS.Timeout>();

  const connect = useCallback(() => {
    const wsUrl = `${import.meta.env.PUBLIC_WS_URL || 'ws://localhost:8000'}/ws/${channel}${token ? `?token=${token}` : ''}`;
    
    try {
      const ws = new WebSocket(wsUrl);
      wsRef.current = ws;

      ws.onopen = () => {
        setIsConnected(true);
        onConnect?.();
      };

      ws.onmessage = (event) => {
        try {
          const message = JSON.parse(event.data) as WebSocketMessage;
          setLastMessage(message);
          onMessage?.(message);
        } catch (e) {
          console.error('Failed to parse WebSocket message:', e);
        }
      };

      ws.onclose = () => {
        setIsConnected(false);
        onDisconnect?.();
        
        if (autoReconnect) {
          reconnectTimeoutRef.current = setTimeout(() => {
            connect();
          }, reconnectInterval);
        }
      };

      ws.onerror = (error) => {
        onError?.(error);
      };
    } catch (e) {
      console.error('WebSocket connection error:', e);
    }
  }, [channel, token, autoReconnect, reconnectInterval, onConnect, onDisconnect, onMessage, onError]);

  const disconnect = useCallback(() => {
    if (reconnectTimeoutRef.current) {
      clearTimeout(reconnectTimeoutRef.current);
    }
    if (wsRef.current) {
      wsRef.current.close();
      wsRef.current = null;
    }
  }, []);

  const sendMessage = useCallback((message: WebSocketMessage) => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify(message));
    }
  }, []);

  useEffect(() => {
    connect();
    return () => disconnect();
  }, [connect, disconnect]);

  return {
    isConnected,
    lastMessage,
    sendMessage,
    connect,
    disconnect,
  };
}

export function useChallengeUpdates(token?: string) {
  return useWebSocket({
    channel: 'challenge_updates',
    onMessage: (message) => {
      if (message.type === 'challenge_update') {
        console.log('Challenge updated:', message.data);
      }
    },
    token,
  });
}

export function useMatchUpdates(token?: string) {
  return useWebSocket({
    channel: 'match_updates',
    onMessage: (message) => {
      if (message.type === 'match_update') {
        console.log('Match updated:', message.data);
      }
    },
    token,
  });
}

export function useStandingsUpdates(token?: string) {
  return useWebSocket({
    channel: 'standings_updates',
    onMessage: (message) => {
      if (message.type === 'standings_update') {
        console.log('Standings updated:', message.data);
      }
    },
    token,
  });
}
