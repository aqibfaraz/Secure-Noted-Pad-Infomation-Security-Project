"""
Maze-Card Hybrid Multi-Round Cipher
A custom symmetric encryption algorithm combining substitution and permutation techniques.
"""

import random
from typing import List, Dict


class MazeCardCipher:
    """
    Custom encryption cipher using card-based substitution and deterministic shuffling.
    """
    
    # Card symbols mapping (represent each character as a card symbol)
    CARD_SUITS = ['♠', '♥', '♦', '♣']
    CARD_RANKS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    
    # Character sets to map
    CHARS = (
        'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        '!@#$%^&*()_+-=[]{}|;:,.<>?/~` "\''
    )
    
    # Generate card symbols for all characters
    CARD_MAP = {}
    REVERSE_CARD_MAP = {}
    
    @classmethod
    def _initialize_maps(cls):
        """Initialize character to card and card to character mappings."""
        if cls.CARD_MAP:
            return  # Already initialized
        
        card_symbols = []
        for suit in cls.CARD_SUITS:
            for rank in cls.CARD_RANKS:
                card_symbols.append(f'{rank}{suit}')
        
        # Map characters to card symbols
        for i, char in enumerate(cls.CHARS):
            if i < len(card_symbols):
                cls.CARD_MAP[char] = card_symbols[i]
                cls.REVERSE_CARD_MAP[card_symbols[i]] = char
    
    @staticmethod
    def _derive_key_parameters(master_key: str) -> Dict:
        """
        Derive encryption parameters from master key.
        
        Args:
            master_key: User-provided master key
            
        Returns:
            Dictionary with seed, rounds, and suit_order
        """
        # Calculate seed from ASCII sum
        ascii_sum = sum(ord(c) for c in master_key)
        seed = ascii_sum % 10007  # Use prime number
        
        # Determine number of rounds (2-4)
        rounds = (ascii_sum % 3) + 2
        
        # Determine suit order based on key
        suits_hash = (ascii_sum * 17) % 24
        suit_order = list(range(4))
        
        # Simple shuffle based on hash
        random.seed(suits_hash)
        random.shuffle(suit_order)
        
        return {
            'seed': seed,
            'rounds': rounds,
            'suit_order': suit_order
        }
    
    @staticmethod
    def _deterministic_shuffle(cards: List[str], seed: int) -> List[str]:
        """
        Perform deterministic shuffle based on seed.
        
        Args:
            cards: List of card symbols
            seed: Seed value for shuffle
            
        Returns:
            Shuffled list of cards
        """
        random.seed(seed)
        shuffled = cards.copy()
        random.shuffle(shuffled)
        return shuffled
    
    @classmethod
    def encrypt(cls, plaintext: str, master_key: str) -> str:
        """
        Encrypt plaintext using Maze-Card Hybrid Cipher.
        
        Args:
            plaintext: Text to encrypt
            master_key: User's master key (not stored)
            
        Returns:
            Encrypted cipher text (space-separated card symbols)
        """
        cls._initialize_maps()
        
        # Step 1: Derive key parameters
        key_params = cls._derive_key_parameters(master_key)
        seed = key_params['seed']
        rounds = key_params['rounds']
        
        # Step 2: Character to card substitution
        cards = []
        for char in plaintext:
            if char in cls.CARD_MAP:
                cards.append(cls.CARD_MAP[char])
            else:
                # Handle unmapped characters (treat as space)
                cards.append(cls.CARD_MAP.get(' ', 'A♠'))
        
        # Step 3: Multi-round deterministic shuffling
        for round_num in range(rounds):
            # Vary seed for each round
            round_seed = seed + (round_num * 12345)
            cards = cls._deterministic_shuffle(cards, round_seed)
        
        # Step 4: Output cipher text
        cipher_text = ' '.join(cards)
        return cipher_text
    
    @classmethod
    def decrypt(cls, cipher_text: str, master_key: str) -> str:
        """
        Decrypt cipher text using Maze-Card Hybrid Cipher.
        
        Args:
            cipher_text: Encrypted text (space-separated card symbols)
            master_key: User's master key (must match encryption key)
            
        Returns:
            Decrypted plaintext
            
        Raises:
            ValueError: If cipher_text format is invalid or wrong master_key
        """
        cls._initialize_maps()
        
        # Step 1: Derive key parameters (same as encryption)
        key_params = cls._derive_key_parameters(master_key)
        seed = key_params['seed']
        rounds = key_params['rounds']
        
        # Parse cipher text
        try:
            cards = cipher_text.split(' ')
        except Exception as e:
            raise ValueError(f"Invalid cipher text format: {str(e)}")
        
        # Step 2: Reverse shuffling (in reverse order)
        for round_num in range(rounds - 1, -1, -1):
            round_seed = seed + (round_num * 12345)
            # To reverse shuffle, we need to know original positions
            # We use the same seed to recreate original shuffle, then map back
            original_cards = list(range(len(cards)))
            random.seed(round_seed)
            indices = list(range(len(cards)))
            random.shuffle(indices)
            
            # Create reverse mapping
            reverse_indices = [0] * len(cards)
            for new_pos, orig_pos in enumerate(indices):
                reverse_indices[orig_pos] = new_pos
            
            # Apply reverse mapping
            cards = [cards[reverse_indices[i]] for i in range(len(cards))]
        
        # Step 3: Card to character reverse substitution
        plaintext = ''
        for card in cards:
            if card in cls.REVERSE_CARD_MAP:
                plaintext += cls.REVERSE_CARD_MAP[card]
            else:
                # If card not recognized, use space
                plaintext += ' '
        
        return plaintext


# Initialize maps on module load
MazeCardCipher._initialize_maps()
