from pathlib import Path
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
import base64

DIR_MODULES = Path(__file__).parent.resolve() / 'modules'

# Key files for RSA public/private key pair
PRIVATE_KEY_FILE = Path(__file__).parent.resolve() / 'private_key.pem'
PUBLIC_KEY_FILE = Path(__file__).parent.resolve() / 'public_key.pem'


def generate_key_pair():
    """Generate RSA public/private key pair"""
    key = RSA.generate(4096)

    # Save private key
    with open(PRIVATE_KEY_FILE, 'wb') as f:
        f.write(key.export_key())

    # Save public key
    with open(PUBLIC_KEY_FILE, 'wb') as f:
        f.write(key.publickey().export_key())

    print(f"Generated new RSA key pair:")
    print(f"  Private key: {PRIVATE_KEY_FILE}")
    print(f"  Public key: {PUBLIC_KEY_FILE}")
    return key


def load_private_key():
    """Load private key for signing"""
    if not PRIVATE_KEY_FILE.exists():
        print("Private key not found, generating new key pair...")
        return generate_key_pair()

    with open(PRIVATE_KEY_FILE, 'rb') as f:
        return RSA.import_key(f.read())


def load_public_key():
    """Load public key for verification"""
    if not PUBLIC_KEY_FILE.exists():
        print("Public key not found, generating new key pair...")
        key = generate_key_pair()
        return key.publickey()

    with open(PUBLIC_KEY_FILE, 'rb') as f:
        return RSA.import_key(f.read())


def create_signature(content: str, private_key: RSA.RsaKey) -> str:
    """Create RSA signature for the content"""
    # Create SHA256 hash of content
    content_hash = SHA256.new(content.encode('utf-8'))

    # Sign with private key using PKCS#1 v1.5
    signature = pkcs1_15.new(private_key).sign(content_hash)

    # Return base64 encoded signature
    return base64.b64encode(signature).decode('utf-8')


def verify_signature(content: str, signature: str, public_key: RSA.RsaKey) -> bool:
    """Verify RSA signature using public key"""
    try:
        # Decode base64 signature
        signature_bytes = base64.b64decode(signature.encode('utf-8'))

        # Create SHA256 hash of content
        content_hash = SHA256.new(content.encode('utf-8'))

        # Verify signature using public key
        pkcs1_15.new(public_key).verify(content_hash, signature_bytes)
        return True
    except Exception:
        return False


def extract_signature_and_content(file_path: Path) -> tuple[str | None, str]:
    """Extract signature from first line and return content without signature"""
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    if not lines:
        return None, ""

    first_line = lines[0].strip()
    if first_line.startswith('# Signature: '):
        signature = first_line[13:]  # Remove '# Signature: '
        content = ''.join(lines[1:])  # Content without signature line
        return signature, content
    else:
        # No signature found
        return None, ''.join(lines)


def sign_file(file_path: Path, private_key: RSA.RsaKey) -> None:
    """Sign a Python file and add signature as first line"""
    print(f"Signing {file_path.name}...")

    # Extract existing content (without signature if present)
    existing_sig, content = extract_signature_and_content(file_path)

    # Create signature for the content
    signature = create_signature(content, private_key)

    # Write file with signature as first line
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(f'# Signature: {signature}\n')
        f.write(content)

    print(f"✓ Signed {file_path.name}")


def sign_all_modules() -> None:
    """Sign all .py files in the modules directory"""
    private_key = load_private_key()

    py_files = list(DIR_MODULES.glob('*.py'))
    if not py_files:
        print("No Python files found in modules directory")
        return

    print(f"Found {len(py_files)} Python file(s) to sign:")
    for py_file in py_files:
        sign_file(py_file, private_key)

    print(f"\n✓ All {len(py_files)} files signed successfully!")


def verify_file(file_path: Path, public_key: RSA.RsaKey) -> bool:
    """Verify signature of a Python file"""
    signature, content = extract_signature_and_content(file_path)

    if signature is None:
        print(f"✗ {file_path.name}: No signature found")
        return False

    if verify_signature(content, signature, public_key):
        print(f"✓ {file_path.name}: Signature valid")
        return True
    else:
        print(f"✗ {file_path.name}: Signature invalid")
        return False


def verify_all_modules() -> bool:
    """Verify signatures of all .py files in the modules directory"""
    public_key = load_public_key()

    py_files = list(DIR_MODULES.glob('*.py'))
    if not py_files:
        print("No Python files found in modules directory")
        return True

    print(f"Verifying {len(py_files)} Python file(s):")

    all_valid = True
    for py_file in py_files:
        if not verify_file(py_file, public_key):
            all_valid = False

    if all_valid:
        print(f"\n✓ All {len(py_files)} files have valid signatures!")
    else:
        print(f"\n✗ Some files have invalid or missing signatures!")

    return all_valid


def show_public_key():
    """Display the public key for distribution"""
    public_key = load_public_key()
    print("Public Key (share this for verification):")
    print("=" * 50)
    print(public_key.export_key().decode('utf-8'))
    print("=" * 50)


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        if sys.argv[1] == "sign":
            sign_all_modules()
        elif sys.argv[1] == "verify":
            verify_all_modules()
        elif sys.argv[1] == "keygen":
            generate_key_pair()
        elif sys.argv[1] == "pubkey":
            show_public_key()
        else:
            print("Usage: python sign-modules.py [sign|verify|keygen|pubkey]")
            print("  sign   - Sign all Python files in modules/")
            print("  verify - Verify signatures of all Python files")
            print("  keygen - Generate new RSA key pair")
            print("  pubkey - Display public key for sharing")
    else:
        # Default: sign then verify
        print("=== SIGNING MODULES ===")
        sign_all_modules()
        print("\n=== VERIFYING SIGNATURES ===")
        verify_all_modules()
