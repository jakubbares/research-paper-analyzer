#!/usr/bin/env python3
"""
Quick test to verify DeepSeek streaming works
"""

import sys
sys.path.insert(0, '/Users/jakubbares/Science/New/paper-analyzer/backend')

from extractors import get_llm_client

def test_streaming():
    print("="*80)
    print("  TESTING DEEPSEEK STREAMING")
    print("="*80)
    
    # Get LLM client (should be DeepSeek if configured)
    llm = get_llm_client()
    
    # Check if streaming is supported
    if not hasattr(llm, 'complete_streaming'):
        print("❌ LLM client doesn't support streaming")
        print(f"   Client type: {type(llm).__name__}")
        return False
    
    print(f"✅ LLM client supports streaming: {type(llm).__name__}")
    
    # Test streaming with a simple prompt
    prompt = """Generate a long HTML document with at least 10 sections. Each section should have:
- A heading
- 3-5 paragraphs of content
- A table with data
- A list of items

Make it information-dense and comprehensive. Don't stop until you've created all 10 sections."""
    
    print("\n🚀 Testing streaming generation...")
    print(f"   Prompt: {prompt[:80]}...")
    
    try:
        chunks = []
        chunk_count = 0
        
        for chunk in llm.complete_streaming(prompt, max_tokens=8192):
            chunks.append(chunk)
            chunk_count += 1
            
            if chunk_count % 50 == 0:
                total_chars = len(''.join(chunks))
                print(f"  📦 Received {chunk_count} chunks, {total_chars} chars so far...")
        
        html = ''.join(chunks)
        
        print(f"\n✅ Streaming complete!")
        print(f"   Total chunks: {chunk_count}")
        print(f"   Total characters: {len(html)}")
        print(f"   Estimated tokens: ~{len(html) // 4}")
        
        # Show first and last 200 chars
        print(f"\n📄 First 200 chars:")
        print(f"   {html[:200]}")
        print(f"\n📄 Last 200 chars:")
        print(f"   ...{html[-200:]}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Streaming test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_streaming()
    sys.exit(0 if success else 1)
