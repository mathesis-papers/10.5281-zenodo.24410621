import hashlib
import json
from math import gcd, isqrt, prod
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def is_prime(candidate):
    return candidate >= 2 and all(candidate % divisor for divisor in range(2, isqrt(candidate) + 1))


def totient(integer):
    result = integer
    remaining = integer
    divisor = 2
    while divisor * divisor <= remaining:
        if remaining % divisor == 0:
            result -= result // divisor
            while remaining % divisor == 0:
                remaining //= divisor
        divisor += 1
    if remaining > 1:
        result -= result // remaining
    return result


def check_siblings():
    specifications = [
        (3, 1, 1, 1, [1]),
        (5, 2, 2, 1, [1]),
        (7, 1, 2, 2, [2, 5]),
        (11, 2, 4, 4, [9, 2, 1, 0]),
    ]
    tables = []
    for prime, offset, tail_period, index_period, expected in specifications:
        modulus = prime - 1
        require(pow(2, modulus, prime) == 1, 'Small-prime exponent period differs')
        require(pow(2, 2 * tail_period, modulus) == pow(2, tail_period, modulus),
                'Small-prime tail period differs')
        require(pow(2, index_period + offset, modulus) == pow(2, offset, modulus),
                'Small-prime index period differs')
        require(pow(2, index_period + offset, tail_period) == pow(2, offset, tail_period),
                'Small-prime inner period differs')
        require(tail_period <= 2 ** offset, 'Small-prime threshold differs')
        residues = [residue_value(prime, modulus, tail_period, offset + residue)
                    for residue in range(index_period)]
        require(residues == expected, 'Small-prime residue table differs')
        tables.append({'prime': prime, 'offset': offset, 'period': index_period, 'values': residues})
    require((2 ** (2 ** 0) + 1) * 2 ** (2 ** (2 ** 0)) - 1 == 11, 'G_0 differs')
    require((2 ** (2 ** 1) + 1) * 2 ** (2 ** (2 ** 1)) - 1 == 79, 'G_1 differs')
    fermat_primes = [2 ** (2 ** index) + 1 for index in range(5)]
    require(all(is_prime(integer) for integer in fermat_primes), 'A small Fermat number is not prime')
    require(641 * 6700417 == 2 ** 32 + 1, 'F_5 factorization differs')
    fermat_modular_cases = 0
    for index in range(10):
        fermat = (1 << (1 << index)) + 1
        require(prod((1 << (1 << previous)) + 1 for previous in range(index)) == fermat - 2,
                'Fermat product identity differs')
        require((1 << (2 * (1 << index))) + 1 == (1 << (1 << (index + 1))) + 1,
                'Binary-to-quaternary identity differs')
        if index >= 2:
            require((1 << index) >= index + 2, 'Hasler exponent divisibility differs')
        for previous in range(index + 1):
            modulus = (1 << (1 << previous)) + 1
            first = pow(2, 1 << index, modulus)
            second = pow(2, 1 << (1 << index), modulus)
            residue = ((first + 1) * second - 1) % modulus
            require(residue == (modulus - 1 if previous == index else 1),
                    'Fermat coprimality residue differs')
            require(gcd(residue, modulus) == 1, 'Fermat coprimality differs')
            fermat_modular_cases += 1
    totient_checks = []
    for index in range(6):
        fermat = (1 << (1 << index)) + 1
        actual = totient(fermat - 2)
        require(actual == (fermat - 1) // 2, 'Totient equality differs at index at most five')
        totient_checks.append({'index': index, 'value': actual})
    product_at_six = prod(totient((1 << (1 << index)) + 1) for index in range(6))
    require(product_at_six < 2 ** 63, 'Totient inequality at index six differs')
    return {'small_prime_tables': tables, 'fermat_primes': fermat_primes,
            'F5_factors': [641, 6700417], 'fermat_congruence_cases': fermat_modular_cases,
            'totient_equalities': totient_checks, 'totient_F6_minus_two': product_at_six,
            'scope': 'Finite premises for the small-prime formulas, Fermat-number identities, and the totient criterion; the corollaries give written all-index proofs.'}


def residue_value(prime, modulus, tail_period, index):
    first_exponent = pow(2, index, modulus)
    second_exponent = pow(2, tail_period + pow(2, index, tail_period), modulus)
    return ((pow(2, first_exponent, prime) + 1) * pow(2, second_exponent, prime) - 1) % prime


def main():
    source = Path(__file__).with_name('certificates.json')
    certificates = json.loads(source.read_text())
    specifications = [('C1', 20, 16, 101), ('C2', 220, 8, 47), ('C3', 72, 32, 149), ('C4', 168, 43, 59)]
    require(len(certificates) == len(specifications), 'Four progression certificates are required')
    exceptional = {('C3', 47): [18], ('C3', 101): [2], ('C4', 47): [26]}
    summaries = []
    total_residues = 0
    total_premises = 0
    for certificate, specification in zip(certificates, specifications):
        label, stride, offset, bound = specification
        require(tuple(certificate[key] for key in ['label', 'stride', 'offset', 'prime_bound']) == specification,
                'Progression statement differs from the specified theorem')
        expected_primes = [candidate for candidate in range(3, bound + 1) if is_prime(candidate)]
        require([row['prime'] for row in certificate['rows']] == expected_primes,
                f'{label}: prime list is incomplete or duplicated')
        rows_checked = 0
        zeros = []
        for row in certificate['rows']:
            prime = row['prime']
            modulus = row['modulus']
            tail_period = row['tail_period']
            index_period = row['index_period']
            require(modulus == prime - 1 and tail_period > 0 and index_period > 0, f'{label}: invalid parameters')
            premises = [
                pow(2, modulus, prime) == 1,
                pow(2, 2 * tail_period, modulus) == pow(2, tail_period, modulus),
                pow(2, stride * index_period + offset, modulus) == pow(2, offset, modulus),
                pow(2, stride * index_period + offset, tail_period) == pow(2, offset, tail_period),
                tail_period <= 2 ** offset,
            ]
            require(all(premises), f'{label}: periodicity premise failed at {prime}')
            total_premises += len(premises)
            values = [residue_value(prime, modulus, tail_period, stride * residue + offset)
                      for residue in range(index_period)]
            zero_indices = [residue for residue, value in enumerate(values) if value == 0]
            expected_zeros = list(range(index_period)) if prime == bound else exceptional.get((label, prime), [])
            require(zero_indices == expected_zeros, f'{label}: unexpected zero set at {prime}')
            if zero_indices:
                zeros.append({'prime': prime, 'period': index_period, 'zeros': zero_indices})
            for residue, value in enumerate(values):
                require(value == residue_value(prime, modulus, tail_period,
                                               stride * (residue + index_period) + offset),
                        f'{label}: shifted residue disagreement')
            rows_checked += len(values)
        total_residues += rows_checked
        summaries.append({'label': label, 'odd_primes': len(expected_primes),
                          'residue_classes': rows_checked, 'zero_sets': zeros})
    for parameter in range(55):
        index = 72 * parameter + 32
        require(((index - 16) % 20 == 0) == (parameter % 5 == 2), 'C1 intersection mismatch')
        require(((index - 8) % 220 == 0) == (parameter % 55 == 18), 'C2 intersection mismatch')
    direct_cases = 0
    for index in range(4):
        integer = (2 ** (2 ** index) + 1) * 2 ** (2 ** (2 ** index)) - 1
        for prime in range(3, 150):
            if is_prime(prime):
                modulus = prime - 1
                tail_period = next(period for period in range(1, 301)
                                   if pow(2, 2 * period, modulus) == pow(2, period, modulus))
                if 2 ** index >= tail_period:
                    require(residue_value(prime, modulus, tail_period, index) == integer % prime,
                            'Direct integer comparison failed')
                    direct_cases += 1
    output = {'status': 'pass', 'certificate_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
              'odd_prime_rows': sum(len(certificate['rows']) for certificate in certificates),
              'periodicity_premises': total_premises, 'residue_classes': total_residues,
              'shifted_residue_comparisons': total_residues, 'intersection_classes': 55,
              'direct_integer_comparisons': direct_cases, 'progressions': summaries,
              'scope': 'Finite modular premises and zero sets for the four progressions; the note proves their all-index consequences.',
              'siblings': check_siblings()}
    print(json.dumps(output, indent=2))


if __name__ == '__main__':
    main()
