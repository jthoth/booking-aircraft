

class Flight(object):

    def __init__(self, number, aircraft):
        self.validations_number_flight(number)
        self._number = number
        self._aircraft = aircraft
        self._seating = self.get_seating()

    def aircraft(self):
        return self._aircraft

    def current_seats(self):
        return self._seating

    def get_seating(self):
        rows, seats = self._aircraft.seating_plan()
        whole_seats = [dict((letter, None) for letter in seats) for _ in rows]

        return [None] + whole_seats

    @staticmethod
    def validations_number_flight(number):
        if not number[:2].isalpha():
            raise ValueError("No airline code in {}".format(number))

        if not number[:2].isupper():
            raise ValueError("Invalid airline code {}".format(number))

        if not number[2:].isdigit():
            raise ValueError("Invalid route number {}".format(number))

        if not int(number[2:]) <= 9999:
            raise ValueError("Invalid route number {}".format(number))

    def number(self):
        return self._number

    def aircraft_model(self):
        return self._aircraft.model()

    def validations_seats(self, seat):
        rows, seats = self._aircraft.seating_plan()
        letter = seat[-1]

        if letter not in seats:
            raise ValueError("Invalid seat letter")
        row = self.get_row(seat)

        if row not in rows:
            raise ValueError("Invalid row nomber {}".format(row))

        return row, letter

    @staticmethod
    def get_row(seat):
        row_text = seat[:-1]

        try:
            row = int(row_text)
        except ValueError:
            raise ValueError("Invalid seat row")

        return row

    def allocate_seat(self, seat, passenger):
        row, letter = self.validations_seats(seat)

        if self._seating[row][letter]:
            raise ValueError("Seat {} already occupied".format(seat))

        self._seating[row][letter] = passenger

    def relocate_seat(self, from_seat, to_seat):

        from_row, from_letter = self.validations_seats(from_seat)
        if self._seating[from_row][from_letter] is None:
            raise ValueError("No passenger to relocate in seat {}".format(from_seat))
        to_row, to_letter = self.validations_seats(to_seat)
        if self._seating[to_row][to_letter]:
            raise ValueError("Seat {} already occupied".format(to_seat))

        self._seating[to_row][to_letter] = self._seating[from_row][from_letter]
        self._seating[from_row][from_letter] = None

    def num_available_seats(self):
        return sum(sum(1 for val in row.values() if val is None)
                   for row in self._seating if row)

    def make_boarding_cards(self, card_printer):
        for passenger, seat in sorted(self._passenger_seats()):
            card_printer(passenger, seat, self._number, self.aircraft_model())

    def _passenger_seats(self):
        row_numbers, seat_letters = self._aircraft.seating_plan()
        for row in row_numbers:
            for letter in seat_letters:
                passenger = self._seating[row][letter]
                if passenger:
                    yield (passenger, '{}{}'.format(row, letter))


class Aircraft(object):

    def __init__(self, registration):
        self._registration = registration

    def registration(self):
        return self._registration

    def num_seats(self):
        rows, letters = self.seating_plan()
        return rows.__len__() * letters.__len__()

    @staticmethod
    def seating_plan():
        return NotImplementedError


class AirbusA319(Aircraft):

    @staticmethod
    def model():
        return "Airbus A319"

    @staticmethod
    def seating_plan():
        return range(1, 23), "ABCDEF"


class Boeing777(Aircraft):

    @staticmethod
    def model():
        return "Boeing 777"

    @staticmethod
    def seating_plan():
        return range(1, 57), "ABCDEFGHIJK"


def make_flight():

    f1 = Flight('BA756', AirbusA319("G-EUPT"))

    f1.allocate_seat('12A', 'Jhon Intriago')
    f1.allocate_seat('15F', 'Mabel Sanchez')
    f1.allocate_seat('15E', 'Belencito')
    f1.allocate_seat('1C', 'Einsten')
    f1.allocate_seat('1D', 'John Nash')

    f2 = Flight('BA756', Boeing777("F-GSPS"))

    f2.allocate_seat('14A', 'Jhon Intriago')
    f2.allocate_seat('14B', 'Mabel Sanchez')
    f2.allocate_seat('15E', 'Belencito')
    f2.allocate_seat('6C', 'Einsten')
    f2.allocate_seat('10K', 'John Nash')

    return f1, f2


def console_card_printer(passenger, seat, flight_number, aircraft):
    output = ("| Name:     {}"
              "  Flight:   {}"
              "  Seat:     {}"
              "  Aircraft: {} |").format(
        passenger, seat, flight_number, aircraft)
    banner = '+' + '-' * (len(output) - 2) + '+'
    border = '|' + ' ' * (len(output) - 2) + '|'
    lines = [banner, border, output, border, banner]
    card = '\n'.join(lines)
    print(card)


if __name__ == '__main__':
    f, g = make_flight()
    print(f.aircraft().num_seats())
    print(g.aircraft().num_seats())
